# Python-SRI
Systeme de recherche d'information avec python (django)

demo : https://sri-tp.herokuapp.com

Screen Shot : 

![Alt Text](/Screen-Shot.png)

### Deploying Python and Django Apps on Heroku
```
$ git add .
$ git commit -m "Added a app."
$ heroku login
$ heroku create
$ git push heroku master
```
### Deploying Python and Django Apps on Google cloud platforme
```
$ git add .
$ git commit -m "Added a app."
$ gcloud app deploy
$ gcloud app browse
```

### install Dependencies
* python
* pip
-----------------------
* Django==1.11.7
* gunicorn==19.7.1
* mongoengine
* pymongo
* nltk
* django-progressive-web-app
* pypandoc==1.3.3
