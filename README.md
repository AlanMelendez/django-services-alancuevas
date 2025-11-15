# Django Services interview

**Disclaimer:** The following setup is for a technical test and is not intended for a production environment.

## Dev requirements to run in linux
Python 3.10+
pip
virtualenv
## Files
req.txt - list of python packages to install successfully run the back

### steps to install requirements
```bash
sudo apt install python3-pip
sudo apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate

### inside of the virtual environment, install requirements
```bash
cd backend
pip install -r req.txt
```

## Steps to create django-project in backend folder
```bash
django-admin startproject django_services_alancuevas .

```

### We need to add the next apps inside of setting.py 
```code
INSTALLED_APPS = [
    ..others,
    "rest_framework",
    "corsheaders"
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware"
]

CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}


```

### Run command below to create the migration
```bash
cd backend
python manage.py migrate

```


## Commands to run project
```bash
cd backend
python manage.py runserver
```



## Create project request for the interview
```bash
cd backend
python manage.py startapp users
python manage.py startapp prompts

```
Add the reference
```code 
INSTALLED_APPS = [
    ...
    "rest_framework",
    "corsheaders",
    "users",
    "prompts",
]
```
## How to try all endpoints

### User Authentication

#### Register a new user

To register a new user, you need to send a POST request to the following endpoint:

```bash
curl -X POST http://localhost:8000/users/register/ -H "Content-Type: application/json" -d '{
    "username": "your_username",
    "password": "your_password"
}'
```

#### Login

To log in and get an access token, send a POST request with your credentials:

```bash
curl -X POST http://localhost:8000/users/login/ -H "Content-Type: application/json" -d '{
    "username": "your_username",
    "password": "your_password"
}'
```
This will return an access and refresh token.

#### Refresh Token
To get a new access token, you can use the refresh token:
```bash
curl -X POST http://localhost:8000/users/token/refresh/ -H "Content-Type: application/json" -d '{
    "refresh": "your_refresh_token"
}'
```

### Prompts

To interact with the prompts endpoints, you need to be authenticated. Use the access token from the login step in the Authorization header.

#### Create a new prompt

```bash
curl -X POST http://localhost:8000/prompts/ -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{
    "text": "This is a new prompt."
}'
```

#### Get similar prompts

To get prompts similar to a given text, you can send a GET request with a `text` parameter:

```bash
curl -X GET "http://localhost:8000/prompts/similar/?text=some text to compare" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## How i'd throw this thing on AWS (kinda)

So, you wanna put this bad boy on the cloud? Aite, bet. Here's a rough sketch of how i'd do it. Don't take this as gospel, it's just a plan, not a production-ready blueprint.

*   **The App (Django):** First, i'd containerize the Django app using Docker. That `docker-compose.yml` is a good start. Then I'd yeet that container onto **AWS Fargate**. Fargate is cool 'cause you don't have to manage any servers. You just give it your container and it runs it. Less headache.

*   **The Database (Postgres):** Instead of running Postgres in a container, I'd use **Amazon RDS**. It's a managed database service. They handle all the boring stuff like backups, patching, and all that jazz. We just connect to it like any other database. 

*   **The Websockets (Redis):** Our websockets need a Redis instance to talk to each other. For that, i'd use **Amazon ElastiCache**. It's basically a managed Redis, same deal as RDS. Set it up, get the connection string, and you're golden.

*   **Traffic Cop (Load Balancer):** To get traffic into our app, i'd set up an **Application Load Balancer (ALB)**. It can handle both the normal HTTP requests and the WebSocket connections. It'll also handle SSL termination, so we get that sweet, sweet `https://`.

*   **Putting it all together (CI/CD):** I'd use **GitHub Actions** to automate everything. When we push to the `main` branch, it would:
    1.  Run the tests (obvs).
    2.  Build the Docker image.
    3.  Push the image to **Amazon ECR** (which is just a private Docker registry).
    4.  Tell Fargate to deploy the new image.

So yeah, that's the gist of it. It's a pretty standard setup and it scales reasonably well.

## Running with Docker

If you wanna skip the local python setup, you can run everything with Docker. It's probably easier.

1.  Make sure you have Docker and Docker Compose installed.
2.  Make sure your `.env` file is ready at the root of the project. You can use the `.env.example` as a template.
3.  Open a terminal at the project root and run:

    ```bash
    docker-compose up --build
    ```
    The first time it might take a while 'cause it has to download and build everything.

Once it's up, you'll have:
*   **The API running at:** `http://localhost:8000`
*   **pgAdmin (to see the database):** `http://localhost:5050`

### How to check the database with pgAdmin

1.  Go to `http://localhost:5050` in your browser.
2.  Log in using the `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` from your `.env` file.
3.  Click on "Add New Server".
4.  In the "General" tab, give it a name you'll remember, like "local-django-db".
5.  Go to the "Connection" tab and fill it out like this:
    *   **Host name/address:** `postgres_db` (this is the name of the service in the `docker-compose.yml`)
    *   **Port:** `5432`
    *   **Maintenance database:** Use the value of `POSTGRES_DB` from your `.env` file.
    *   **Username:** Use the value of `POSTGRES_USER` from your `.env` file.
    *   **Password:** Use the value of `POSTGRES_PASSWORD` from your `.env` file.
6.  Hit "Save".

And that's it! You should now be able to browse your database, see the tables Django made, and whatever data gets saved.
