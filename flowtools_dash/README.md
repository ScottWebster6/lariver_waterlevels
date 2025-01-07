To run this, you will need to install Python and a few dependencies first.

Installing Python is straightforward. 
(see: https://www.python.org/downloads/)

Installing dependencies in Python is not. 

1/7/2025 Release:
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

Extra things I could do by January 7th:
    0. Fix any bugs!!!
    1. Add light/dark theme switcher
    2. Match heights? Test in Colab first. 
    4. Optimize program, make sure callbacks aren't ran more than necessary. 


Things to do later:
    0. Install Gunicorn and use it to host over LAN
    1. Use a better environment manager (conda, pipenv, docker, etc)
    2. Set up more advanced caching techniques
        * Redis Caching?
        * Look into Dash Extensions ServersideOutputTransform? 
    3. Implement Job Queues a la Dash Enterprise
    4. Implement a big data pipeline from SQLite, Databricks, etc
        * Currently, we just load CSV files from a public github repository.
          This will fail us when we need bigger data/need to load in chunks of data.