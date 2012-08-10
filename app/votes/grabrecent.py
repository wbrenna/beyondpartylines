#from lxml import etree
import xml.etree.ElementTree as etree
import urllib2

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

def getcurrentsitting(cursitting,csitting):
	sitting = open(cursitting,"r")
	csitting.parl = int(sitting.readline())
	csitting.ses = int(sitting.readline())
	csitting.last = int(sitting.readline())
	sitting.close()


def savecurrentsitting(currentsitting,cursitting):
	sitting = open(cursitting,"w")
	sitting.write(str(currentsitting.parl));
	sitting.write("\n")
	sitting.write(str(currentsitting.ses));
	sitting.write("\n")
	sitting.write(str(currentsitting.last));
	sitting.close()



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
			print "Error downloading/parsing %s" % xmlurl
			print e
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
			recentvotes(currentsitting,0,cursitting)
	except Exception, e:
		print "Error downloading/parsing %s" % xmlurl
		print e


	xmlurl = XML % {'parliamentnum' : currentsitting.parl+1, 'sessnum' : 1, 'votenum' : 1}
	try:
		myxml = urllib2.urlopen(xmlurl)
		tree = etree.parse(myxml)
		root = tree.getroot()
		if root.find('Decision') is not None:
			currentsitting.parl += 1
			currentsitting.ses = 1
			recentvotes(currentsitting,0,cursitting)
	except Exception, e:
		print "Error downloading/parsing %s" % xmlurl
		print e




def go():
	cursitting = 'currentsitting.dat'
	datadir = 'app/db/'
	currentsitting = parliamentdatastructs.currentsessionofparliament()
	getcurrentsitting(cursitting,currentsitting)
	recentvotes(currentsitting,datadir,cursitting)



