#from lxml import etree
import xml.etree.ElementTree as etree
import urllib2
import json
import os

import parliamentdatastructs


def none_to_empty(s):
    return s if s is not None else ''	

def etree_extract_text(elem):
    text = ''
    for x in elem.getiterator():
        if text and x.tag in ('Para', 'P', 'p'):
            text += "\n\n"
        text += (none_to_empty(x.text) + none_to_empty(x.tail)).replace("\n", ' ')
    return text

def getcurrentsitting(cursitting,csitting,oldsitting):
	if os.path.exists(cursitting):
		sitting = open(cursitting,"r")
		csitting.parl = int(sitting.readline())
		csitting.ses = int(sitting.readline())
		csitting.last = int(sitting.readline())
		sitting.close()
		oldsitting.parl = csitting.parl
		oldsitting.ses = csitting.ses
		oldsitting.last = csitting.last
#Now grab the most recent to check how long you've been away.
		mostrecentsitting = parliamentdatastructs.currentsessionofparliament()
		grabmostrecent(mostrecentsitting)
		if ((mostrecentsitting.parl != csitting.parl) or (mostrecentsitting.ses != csitting.ses) or (mostrecentsitting.last - csitting.last > 50)):
			print 'Much more recent sitting detected.'
			csitting.parl = mostrecentsitting.parl
			csitting.ses = mostrecentsitting.ses
			csitting.last = mostrecentsitting.last
			return False
		return True
	else:
#the file does not exist - we'll grab the most recent sitting
		print 'Current sitting file does not exist. Creating sitting file for current date.'
		grabmostrecent(csitting)
		return True

def savecurrentsitting(currentsitting,cursitting):
	sitting = open(cursitting,"w")
	sitting.write(str(currentsitting.parl));
	sitting.write("\n")
	sitting.write(str(currentsitting.ses));
	sitting.write("\n")
	sitting.write(str(currentsitting.last));
	sitting.close()

def grabmostrecent(rsitting):
	JSON1 = 'http://api.openparliament.ca/votes/?offset=1&limit=1&format=json'
	#JSON2 = 'http://api.openparliament.ca/debates/?offset=1&limit=1&format=json'
#The first contains the session while the second contains the sitting.
	response = urllib2.urlopen(JSON1)
	session1 = json.load(response)['objects'][0]['session'].split('-')
	#response = urllib2.urlopen(JSON2)
	response = urllib2.urlopen(JSON1)
	#sitting1 = json.load(response)['objects'][0]['number']
	session2 = json.load(response)['objects'][0]['number']
	
	rsitting.parl = int(session1[0])
	rsitting.ses = int(session1[1])
	#rsitting.last = int(sitting1)
	rsitting.last = int(session2)

def checksitting(csitting):
	csitting.parl = int()
	csitting.ses = int()
	csitting.last = int()


def recentvotes(currentsitting,datadir,cursitting):
	XML = 'http://www2.parl.gc.ca/HouseChamberBusiness/Chambervotedetail.aspx?Language=E&Mode=1&Parl=%(parliamentnum)s&Ses=%(sessnum)s&FltrParl=%(parliamentnum)s&FltrSes=%(sessnum)s&vote=%(votenum)s&xml=True'

	votedata = parliamentdatastructs.votedata()

	y = currentsitting.last + 1

	while(True):
		xmlurl = XML % {'parliamentnum' : currentsitting.parl, 'sessnum' : currentsitting.ses, 'votenum' : y}
		try:
			myxml = urllib2.urlopen(xmlurl)
			tree = etree.parse(myxml)
		except Exception, e:
			try:
				y += 1
				xmlurl = XML % {'parliamentnum' : currentsitting.parl, 'sessnum' : currentsitting.ses, 'votenum' : y}
				myxml = urllib2.urlopen(xmlurl)
				tree = etree.parse(myxml)
			except Exception, e:
				#print "No vote exists at %s" % xmlurl
				#print e
				y -= 1
				break


		root = tree.getroot()

		votedata.decision = root.find('Decision').text

		if root.find('Title') is not None:
			votedata.title = root.find('Title').text
		else:
			votedata.title = ''
		if root.find('RelatedBill') is not None:
			votedata.bill = root.find('RelatedBill').attrib['number']
		else:
			votedata.bill = ''


		votedata.description = etree_extract_text(root.find('Context')).strip()
		votedata.vote = str(y)

		filename = datadir + str(currentsitting.parl) + '_' + str(currentsitting.ses) + '_' + votedata.vote + '.txt'
		fn = open(filename,"w")
		fn.write(votedata.vote.encode('utf-8'))
		fn.write("\n")
		fn.write(votedata.bill.encode('utf-8'))
		fn.write("\n")
		fn.write(votedata.title.encode('utf-8'))
		fn.write("\n")
		fn.write(votedata.decision.encode('utf-8'))
		fn.write("\n")
		fn.write(votedata.description.encode('utf-8'))
		fn.close()

		y += 1

	currentsitting.last = y-1
	savecurrentsitting(currentsitting,cursitting)

#Check for future sessions/parliaments in case we are missing something!
	xmlurl = XML % {'parliamentnum' : currentsitting.parl, 'sessnum' : currentsitting.ses+1, 'votenum' : 1}
	try:
		myxml = urllib2.urlopen(xmlurl)
		tree = etree.parse(myxml)
		root = tree.getroot()
		if root.find('Decision') is not None:
			currentsitting.ses += 1
			currentsitting.last = 1
			recentvotes(currentsitting,0,cursitting)
	except Exception, e:
		#print "No vote exists at %s" % xmlurl
		#print e
		pass


	xmlurl = XML % {'parliamentnum' : currentsitting.parl+1, 'sessnum' : 1, 'votenum' : 1}
	try:
		myxml = urllib2.urlopen(xmlurl)
		tree = etree.parse(myxml)
		root = tree.getroot()
		if root.find('Decision') is not None:
			currentsitting.parl += 1
			currentsitting.ses = 1
			currentsitting.last = 1
			recentvotes(currentsitting,0,cursitting)
	except Exception, e:
		#print "No vote exists at %s" % xmlurl
		print "We have probably downloaded all available votes. If you are unsure please view currentsitting.dat and compare with openparliament.ca." 




def go(cursitting,datadir,currentsitting):
	#cursitting = 'currentsitting.dat'
	#datadir = 'app/db/'
	#currentsitting = parliamentdatastructs.currentsessionofparliament()
	#getcurrentsitting(cursitting,currentsitting)
	recentvotes(currentsitting,datadir,cursitting)



