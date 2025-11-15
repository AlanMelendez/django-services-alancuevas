# Let's start with a slim Python image so it's not too heavy
FROM python:3.10-slim

# A couple of environment variables to make Python behave
# Don't create those annoying .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# And print everything straight to the console no waiting
ENV PYTHONUNBUFFERED 1

# This is where our app will live inside the container
WORKDIR /app

# First, we copy only the requirements...
COPY req.txt /app/
# ...and install them... This way Docker can cache this step if they don't change.
RUN pip install --no-cache-dir -r req.txt

# Now let's copy all the app code
COPY . /app/
