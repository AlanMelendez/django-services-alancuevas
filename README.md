# Django Services interview

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
```code
cd backend
python manage.py migrate

```
