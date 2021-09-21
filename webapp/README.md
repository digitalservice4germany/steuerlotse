# Steuerlotse Flask backend

## Getting started 🛠

For developing, we suggest running the Flask app locally. Assuming that you are on a UNIX-like OS, the following 
commands should get you up and running:

```bash
cd webapp/

# Install Python dependencies
pipenv install

# Install client-side dependencies
cd client/ && yarn install && cd ..

# Ensure required environment variables are set
cp .env.example .env

# Initialize local database
pipenv run flask db upgrade
pipenv run flask populate-database

# Generate translation files
./scripts/babel_run.sh
```

## Development 👩‍💻 👨‍💻

To develop the app, you need to run two process: 1) the Flask app and 2) a dev server for client-side components.

### Starting the Flask app

```bash
cd webapp/
pipenv run flask run
```

### Starting the client-side dev server

```bash
cd webapp/client/
yarn start
```

You can now interact with the website on http://localhost:3000.

[See here for more detailed information about developing client-side components.](client/README.md)

### Updating translation files

After every translation change (new strings, updated .po file) and also during first-time setup, run:

```bash
cd webapp/
./scripts/babel_run.sh
```

### Using the Erica Mock service
A large amount of functionality in the app also requires a local erica service to be running.

If you _do not want to run erica_ at the same time, you can set `USE_MOCK_API = True` in the `DevelopmentConfig` in the webapp's `config.py`.

## Testing 📃

You can run tests as follows:
```bash
cd webapp/
pipenv run pytest
```

## Making changes to the database schema ⛓

For database migration and upgrades, we use Flask-Migrate. Make sure that you are in the pipenv shell and then do:

````bash
cd webapp/
# After model has been changed
flask db migrate  # Creates a new migration script in migrate/versions
flask db upgrade  # Updates the database using the migration script
````
⚠️ Flask-Migrate uses Alembic. Alembic does not detect all changes to the model (especially renaming tables or columns).
Therefore re-check the migration script. You can find a list of Alembic's limitations 
[here](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).
