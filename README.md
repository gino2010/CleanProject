Clean Project for web server application and Hybrid Mobile
=============
Version: 2.0 beta

Clean Server
-------------
### Function:
Clean server project for deployment, like Django web server application project

1. Remove .py keep .pyc, remove .idea and .git directory
2. Adds and removes AngularJS dependency injection annotations by [ng-annotate]
3. Compress js and css file yuicompressor(choose one)
  * You need to install youcompressor package by pip
  * You can download [yuicompressor] put yuicompressor.jar in java classpath or with main.py in same diretory
4. Output cleaned project files in 'clean_deployment' directory

### Usage:
1. deal with current directory, in project root directory:
```
python cleanServer.py
```
2. deal with specify directory:
```
python cleanServer.py /your/directory/
```

Clean Mobile
-------------
### Function:
Clean hybrid mobile for build, like HTML5 + Angularjs hybrid mobile client application

Notice: only support android project now

1. Remove .idea and .git directory
2. Transform angular js files in www directory by [ngmin] to prepare to compress
3. Compress js file by yuicompressor(choose one)
  * You need to install youcompressor package by pip
  * You can download [yuicompressor] put yuicompressor.jar in java classpath or with main.py in same diretory
4. Output cleaned project files in 'clean_mobile' directory

### Usage:
1. deal with current directory, in project root directory:
```
python cleanMobile.py
```
2. deal with specify directory:
```
python cleanMobile.py /your/directory/
```

License
-------------
GPL

[ng-annotate]:https://github.com/olov/ng-annotate
[yuicompressor]:https://github.com/yui/yuicompressor/releases
[ngmin]:https://github.com/btford/ngmin