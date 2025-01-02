To run this, you will need to install Python and a few dependencies first.

Installing Python is straightforward. 
Installing dependencies in Python is not.

It is preferred to run third-party python packages in a virtual environment,
(see: https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)
(also works for mac and other POSIX-compliant systems)
but if you don't feel like doing that then you can just run the commands:

 $pip install -r requirements.txt 
 
And then proceed to launch our program locally with:

 $python flowtools.py 

Clicking on the link that appears in the terminal will to open in a
browser to function as localhost browser window.

This is "good enough" for now until we have secured a domain name. 
We should use a better environment manager (conda, pipenv, etc) later.

Things to do later:
    1. Use a better environment manager (conda, pipenv, etc)
    2. Set up more advanced caching techniques
        * Redis Caching?
        * Look into Dash Extensions ServersideOutputTransform? 
    3. Implement Job Queues a la Dash Enterprise
    4. Implement a big data pipeline from SQLite, Databricks, etc. 