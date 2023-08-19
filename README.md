# Django Scoring App

Django app to keep scores in boardgames like Agricola or Wingspan.

## Deployment to pythonanywhere

NOTE: After deployment, anyone can visit the app here: http://danielcaballero88.pythonanywhere.com/

Create a tarball with the django app leaving the DB out (we don't want to overwrite the sqlite db each time we deploy).

```bash
rm -r /tmp/django-scoring-app
mkdir /tmp/django-scoring-app
tar --exclude='db.sqlite3' -czvf /tmp/django-scoring-app/app.tar.gz ./*
```

Go to https://www.pythonanywhere.com/login/?next=/user/danielcaballero88/webapps/#tab_id_danielcaballero88_pythonanywhere_com
 
Upload the file to home, remove everything in the `app` folder, except the db, and extract the uploaded file into the `app` folder:

```bash
cd ~/app
mv db.sqlite3 ../
rm -r *
cp ../app.tar.gz ./
tar -xzvf app.tar.gz
rm app.tar.gz
mv ../db.sqlite3 ./
```

Finally, but VERY IMPORTANT, go into `mysite/settings.py` and change `DEBUG` to `False`.

### Static files

Make sure to run `collectstatic` if there were changes to the static files.
This will put any static files in the `assets` directory and that is mapped to the static url `/assets/` in the settings file.
Otherwise no css or js or images will be served correctly.

### Virtual environment

Make sure to reinstall requirements if there were changes to them.
The virtualenv in use is `django-scoring-app-virtualenv`.