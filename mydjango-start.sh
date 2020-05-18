# Create a virtual environment to isolate our package dependencies locally
python3.6 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtual environment
pip3 install django
pip3 install djangorestframework

# Set up a new project with a single application
django-admin startproject cparking  # Note the trailing '.' character
cd cparking
django-admin startapp parkapp
cd ..
