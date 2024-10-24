# Example Django Project


```bash
git clone 'https://github.com/ArchiveBox/pydantic-pkgr'
cd pydantic-pkgr

pip install -e .             # install pydantic_pkgr from source

cd django_example_project/   # then go into the demo project dir

./manage.py makemigrations   # create any migrations if needed
./manage.py migrate          # then run them to create the demo sqlite db
./manage.py createsuperuser  # create an admin user to test out the UI

./manage.py runserver        # then open http://127.0.0.1:8000/admin/
```
