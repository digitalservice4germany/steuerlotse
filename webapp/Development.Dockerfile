FROM python:3.9.10 as webapp

WORKDIR /app

RUN pip install --upgrade pip pipenv flask python-dotenv
COPY ./Pipfile ./Pipfile.lock ./
RUN pipenv install --system
RUN rm .env -f
# Now copy in our code, and run it
COPY . .
EXPOSE 8000
CMD ["python","-m","flask", "run", "--debugger", "--host=0.0.0.0"]