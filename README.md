Clean Project for python and web server application
=============
Version: 1.0

Function
-------------
Clean project for deployment

1. Remove .py keep .pyc
2. Compress js and css file depend on yuicompressor 2.4.8
  * yuicompressor: https://github.com/yui/yuicompressor/releases
  * You can put yuicompressor.jar in java classpath or with main.py in same diretory
3. Output cleaned project files in 'deployment' directory

Usage
-------------
1. deal with current directory: python main.py 
2. deal with specify directory: python main.py /your/directory/
