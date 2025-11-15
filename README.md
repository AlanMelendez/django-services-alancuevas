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

```
