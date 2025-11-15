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
