BeyondPartyLines
===============

This suite will prompt you at your leisure for your personal voting decisions, 
logging these and allowing you to compare them with Canadian Members of Parliament. 
Become a member of the House of Commons! 




Install
=======

If you are fortunate enough to have acquired a binary/executable for the program 
(there might be some at 
[wbrenna.uwaterloo.ca](http://wbrenna.uwaterloo.ca/wilson/projects/beyondpartylines.php)), 
simply launch it. Otherwise, you will need Python (I used Python2.6, your results 
may vary with other versions) and a few dependencies:

	BeautifulSoup
	matplotlib
	numpy
	pyttk (which requires Tk wrappers for Python)

The easiest method of installation on systems with a good package manager (for example, 
apt). Here, simply install the prerequisites:

```bash
sudo apt-get install python-numpy python-matplotlib python-tk python-beautifulsoup
```

Then, run the application with

```bash
python beyondpartylines.py
```


If, for some reason, you cannot install the dependencies as above, this application 
can be setup in two other ways (see below for additional install notes).

Run
====

The application window will pop up. Initially the list of votes will be unpopulated. 
Click "Download" to download votes from the last vote in currentsitting.dat. The 
window should be populated with votes from the House of Commons, last to first.

More help is provided from the Help menu in program. 


Hinton Plots
-------------

The Hinton plot deserves a little explaining. This plot allows for the
visualization of your votes versus another MPs. Currently the axes are not
labelled but the votes begin from the top left (the highest number of bill-vote
you have voted Yes, No, or Abstain on) and travel left-to-right, top-to-bottom,
in the order of decreasing vote number. The reason labelling is nontrivial is
because you may have skipped votes, and vote data may go between parliamentary
sittings. For example, if you voted on issues 445, 440, 441, and 404, the Hinton
plot would be a 2x2 grid as follows:

	445	441
	440	404

A large white box means you voted the same way as the MP (Yes-Yes or No-No). A
black large box means you directly opposed one another (Yes-No). The small white
box means you abstained and the MP voted, while a small black box means you
voted and the MP abstained. An empty grey square means you both abstained, or,
since the plot must be square, it is filler for the remainder of the plot space.
At the top, the correlation index is specified, to say how often you agreed with
the MP.


Installation Details
====================

Install with pip
----------------

First, ensure you have pip and virtualenv installed. Start a virtualenv with 

```bash
virtualenv --no-site-packages bpl_env
. bpl_env/bin/activate
```

Then, you can install the packages required with 

	pip install -r pipdeps.txt

If you get an error like this:

	BUILDING MATPLOTLIB

            matplotlib: 1.1.0
                python: 2.6.6 (r266:84292, Dec 26 2010, 22:31:48)  [GCC 4.4.5]
              platform: linux2

	REQUIRED DEPENDENCIES

                 numpy: no
                        * You must install numpy 1.1 or later to build
                        * matplotlib.
		
you likely have to install numpy first. This is a known bug in pip, and it also
occurs with setuptools (below), meaning you have to satisfy the numpy
dependencies before the installation will go on. You simply need to run

	pip install numpy

followed by 

	pip install -r pipdeps.txt

Then, while you are still in the virtualenv, you can run the software with

	python beyondpartylines.py

To exit the virtualenv, type

	deactivate

and to reenter the virtualenv (to run the software again) run

```bash
. bpl_env/bin/activate
```

again. It is that easy!


Install with setuptools
-----------------------

This option will automatically install setuptools for you, if you do not have
it. You will likely have to preinstall numpy (see above).

```bash
sudo python setup.py install
```

I have never actually been able to get this approach to work, since building numpy 
and matplotlib with setuptools has always broken on my systems. One thing that
may help would be installing the Python headers (python2.6-dev on my system).



Lingering Errors
----------------

If you still have problems, feel free to send me an email. One issue that
appears common on Ubuntu is the error

	No module named _tkagg

or similar. This can be fixed by removing the matplotlibrc file or by changing
the backend specified in matplotlibrc.



