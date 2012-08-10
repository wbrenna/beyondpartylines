BeyondPartyLines
===============

This suite will prompt you at your leisure for your personal voting decisions, 
logging these and allowing you to compare them with Canadian Members of Parliament. 
Become a member of the House of Commons! 




Install
=======

If you are fortunate enough to have acquired a binary/executable for the program (there might be some at <wbrenna.uwaterloo.ca/projects/beyondpartylines.php>), 
simply launch it. Otherwise, you will need Python (I used Python2.6, your results 
may vary with other versions) and a fair list of dependencies, such as 

	BeautifulSoup,
	matplotlib,
	numpy,
	pyttk


Run the application with

	python beyondpartylines.py


Equivalently, this application can be setup with setuptools by running

	python setup.py



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
