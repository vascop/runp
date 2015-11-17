runp
====

.. image:: https://travis-ci.org/vascop/runp.svg
    :target: https://travis-ci.org/vascop/runp

.. image:: https://coveralls.io/repos/vascop/runp/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/vascop/runp?branch=master


runp exports Python functions from files to the command line. 
You don't need to change your existing code.

If you have a file named myfile.py with::

    def foo():
        """beeps a lot"""
        print "beep beep"

    def bar(text):
        """Prints things

        Args:
            text (str): The text to print
        """
        print text

And you want to run it in the command line just do::

    $ runp myfile.py foo
    beep beep

You can also pass arguments to your functions::

    $ runp myfile.py bar:"this is sweet!"
    this is sweet!

Functions with names starting with _ are hidden. 

You can list available functions with::

    $ runp myfile.py -l
    Available functions:
    foo    beeps a lot
    bar    Prints things

And get info on a specific function::

    $ runp myfile.py -d bar
    Displaying docstring for function bar in module myfile

    bar(text)
        Prints things
    
        Args:
            text (str): The text to print

Syntax for calling functions is::
    
    $ runp myfile.py function_name:arg1value,arg2=arg2value


The concept, syntax for commands and initial code are heavily inspired by fabric's task system.