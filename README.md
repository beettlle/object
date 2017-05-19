# Object

The point of Object is to help make it easy for people to create CRUD application without having to know much coding.  All that is needed is to add a new JSON file in the right place with the proper description and you're good to go!

To create a new object:
 - Look at the examples	under [static/json](static/json) for inspiration
 - Create a new file with the name of the Object you want to track
 - Add fields you'd like the object you're trying to add

To install:
 - Change directory to the 'object' directory
 - Create a `virtualenv` with for python 2.7
 	- `virtualenv -p /usr/bin/python2.7 .venv`
 - Run that virtualenv
 	- `. .venv/bin/activate`
 - Install all the requirements
 	- `pip install -r resources.txt`

To run:
 - Start the application
 	- `python main.py`
 - Point your browser to [localhost:8888](http://localhost:8888)
