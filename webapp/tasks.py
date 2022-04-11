import subprocess
import time

from invoke import task


CLIENT_DIR = "client/"


def wait_until_up(url, max_tries=100, delay=0.1):
    import requests

    try_num = 0
    while try_num < max_tries:
        try:
            requests.get(url)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(delay)
            try_num += 1
    raise RuntimeError(f"Maximum retries for connecting to {url} exceeded.")


@task
def start_test_server(c, webapp_dir=None):
    import sarge

    if webapp_dir is None:
        webapp_dir = c.cwd

    env = {
        'FLASK_ENV': 'functional',
        'CI': 'true',
        'BROWSER': 'none',  # stop `yarn start` from trying to open a browser window
        'SESSION_DATA_STORAGE_URL': 'redis:127.0.0.1:6379'
    }

    # Set up DB
    sarge.run("flask db upgrade", cwd=webapp_dir, env=env)
    sarge.run("flask populate-database", cwd=webapp_dir, env=env)
    sarge.run("./scripts/babel_run.sh", cwd=webapp_dir, env=env)
    
    # Set up Redis
    c.run("docker run --name redis -p 6379:6379 -d redis", env=env)
        
    # Run flask server
    sarge.run("flask run", cwd=webapp_dir, env=env, async_=True)
    wait_until_up('http://localhost:5000')
    # Run React dev-server
    sarge.run("yarn start", env=env, async_=True, stdout=subprocess.DEVNULL)
    wait_until_up('http://localhost:3000')


@task
def test_pytest(c):
    c.run("pytest -n auto")


@task
def test_client_unit(c):
    with c.cd(CLIENT_DIR):
        c.run("yarn test", env={'CI': 'true'})  # CI=true forces all tests to run


@task
def test_functional_run(c):
    test_functional(c, "run")


@task
def test_functional_ui(c):
    test_functional(c, "ui")


@task
def test_functional(c, mode):
    import psutil
    import sarge

    env = {
        'FLASK_ENV': 'functional',
        'CI': 'true',
        'BROWSER': 'none',  # stop `yarn start` from trying to open a browser window
        'SESSION_DATA_STORAGE_URL': 'redis:127.0.0.1:6379'
    }

    # Set up DB
    c.run("flask db upgrade", env=env)
    c.run("flask populate-database", env=env)
    c.run("./scripts/babel_run.sh", env=env)
    
    # Set up Redis
    c.run("docker run --name redis -p 6379:6379 -d redis", env=env)

    try:
        # Run flask server
        flask_pipeline = sarge.run("flask run", env=env, async_=True)
        wait_until_up('http://localhost:5000')
        # Run React dev-server
        react_pipeline = sarge.run("yarn start", cwd=CLIENT_DIR, env=env, async_=True, stdout=subprocess.DEVNULL)
        wait_until_up('http://localhost:3000')

        # Run functional tests
        with c.cd(CLIENT_DIR):
            c.run("yarn test:functional-" + mode, env=env)

    finally:
        # Shut down started processes
        if flask_pipeline:
            cmd = flask_pipeline.commands[0]
            cmd.terminate()
        if react_pipeline:
            cmd = react_pipeline.commands[0]
            # For some reason, terminating the command leaves a dangling child process, so we kill them manually.
            for child in psutil.Process(cmd.process.pid).children(recursive=True):
                child.terminate()
            cmd.terminate()

        # Delete test database
        c.run("rm ./app/functional-testing.db")
        
        # Stop redis
        c.run("docker stop $(docker ps -q --filter ancestor=redis)", env=env)


@task(test_pytest, test_client_unit, test_functional_run)
def test(c):
    """This no-op task triggers all test suites as dependencies."""
    pass


@task
def lint(c):
    # fail the build if there are Python syntax errors or undefined names
    c.run("flake8 . --count --select=E9,E112,E113,E117,E711,E713,E714,F63,F7,F82 --show-source --statistics")
    # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
    c.run("flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics")
