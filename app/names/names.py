from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re
from app.votes import parliamentdatastructs
import xml.etree.ElementTree as etree
from app.gui import plot


def searchforkey(string):
	URL = "http://www.parl.gc.ca/Search/Results.aspx?Language=E&search_term=%s" % string.replace(" ", "%20")
	key = ""
	urlname = ""
	print URL
	try:
		searchresult = BeautifulSoup(urllib2.urlopen(URL),parseOnlyThese=SoupStrainer('a'))
	except Exception, e:
		print e
		return ""
	myresult =  searchresult.findAll(href=re.compile("http://www.parl.gc.ca/Parliamentarians/en/members/.*\(.*\)"))
	for result in myresult:
		key = re.findall(r'\d+',result['href'])[0].encode('utf-8')
		urlname = re.findall(r'\/[A-Za-z]*-[A-Za-z]*\(',result['href'])[0].encode('utf-8')[1:-1]
		break
	print key
	print urlname
	
	return [key,urlname]


def searchforvote(xmltree,votenum,counter):
	i = counter[0]
	root = xmltree.getroot()
	#mpvotes = root.findall("Vote")
	mpvotes = root.findall("VoteParticipant")
	#firstvote = int(mpvotes[0].attrib['number'])
	firstvote = int(mpvotes[0].find('DecisionDivisionNumber').text)
	votenum2 = int(votenum)
	if (firstvote > votenum2):
#This means the starting vote doesn't yet exist in the database.
#For now mark it as abstain, just like missing votes.
		return 0
	myvote = mpvotes[firstvote + i]
	myvotenum = int(myvote.find('DecisionDivisionNumber').text)
	#print "Parsing MP vote ",myvote.find('DecisionDivisionNumber').text," and user vote ",votenum2
	print "Parsing vote ",votenum2
	if (myvotenum < votenum2):
		while (myvotenum < votenum2):
#			print counter[0], myvote.attrib['number'], votenum2
			i += 1
			myvote = mpvotes[firstvote + i]
			myvotenum = int(myvote.find('DecisionDivisionNumber').text)
	elif (myvotenum > votenum2):
                while (myvotenum > votenum2):
#			print counter[0], myvote.attrib['number'], votenum2
                        i -= 1
                        myvote = mpvotes[firstvote + i]
			myvotenum = int(myvote.find('DecisionDivisionNumber').text)
	counter[0] = i
	#print "Final value:", counter[0], myvote.find('DecisionDivisionNumber').text, votenum2

	if (int(myvote.find('DecisionDivisionNumber').text) != int(votenum)):
#This means we couldn't find the vote - Abstain!
		#print "Couldn't find vote - we were at %(mv)s which didn't match the wanted vote number %(vn)s." % {'mv' : str(myvote.attrib['number']), 'vn' : votenum}
		print "This politician didn't vote on vote number ", int(votenum)
		return 0

	#if myvote.find("RecordedVote").find("Yea").text == "1":
	votestate = myvote.find("VoteValueName").text
	if votestate == "Yea":
		print ":yea"
		return 1
	elif votestate == "Nay":
		print ":nea"
		return -1
	elif votestate == "Paired":
#For now, I mark paired as the same as abstain
		return 0

	else:
		print "There appears to have been an error. Vote data may not be reliable."
		return 0	

def sesstoSessionId(ses, parl):
	sesval = parl*10 + ses

	if sesval == 381:
		return 140
	elif sesval == 391:
		return 141
	elif sesval == 392:
		return 142
	elif sesval == 401:
		return 143
	elif sesval == 402:
		return 145
	elif sesval == 403:
		return 147
	elif sesval == 411:
		return 150
	elif sesval == 412:
		return 151
	else:
		print "There was an error converting to SessionId. Please contact the developer!"
		return -1

def plotvotes(key,urlname):
	#URL = "http://www.parl.gc.ca/MembersOfParliament/ProfileMP.aspx?key=%(thekey)s&SubSubject=1006&Language=E&FltrParl=%(parlnum)s&FltrSes=%(sessnum)s&VoteType=0&AgreedTo=True&Negatived=True&Tie=True&Page=1&xml=true&SchemaVersion=1.0"
	URL = "http://www.parl.gc.ca/Parliamentarians/en/members/%(theurlname)s(%(thekey)s)/ExportVotes?sessionId=%(sessnum)s&output=XML"
	filename = "votes.dat"
	filehndl = open(filename,"r")
	lines = []

	while 1:
		line = filehndl.readline()
		if not line:
			break
		lines.append(line.rstrip())
	
	oldsess = ""
	oldparl = ""
	oldkey = 0
	correlation = []
	vdata = parliamentdatastructs.votedata()
	counter = []
	tree = ""
	for line in lines:
		tmp = line.split(' ')
		vdata.ses = tmp[1]
		vdata.parl = tmp[0]
		if (oldsess == vdata.ses) and (oldparl == vdata.parl) and (oldkey == key):
#only download the XML file if we need to
			vdata.vote = tmp[2]
			vdata.decision = tmp[3]
		else:
#download the XML file
			#xmlURL = URL % {'parlnum' : vdata.parl, 'sessnum' : vdata.ses, 'thekey' : key}
			xmlURL = URL % {'theurlname' : urlname, 'sessnum' : sesstoSessionId(int(vdata.ses),int(vdata.parl)), 'thekey' : key}
			try:
				myXML = urllib2.urlopen(xmlURL)
				tree = etree.parse(myXML)
			except Exception, e:
				print "Error downloading/parsing %s" % xmlURL
				print e
				return 1
			oldsess = vdata.ses
			oldparl = vdata.parl
			oldkey = key
			counter.append(0)

		vdata.vote = tmp[2]
		vdata.decision = tmp[3]
		mpvote = searchforvote(tree,vdata.vote,counter)
		
		if ((vdata.decision == "Yes") and (mpvote == 1)) or ((vdata.decision == "No") and (mpvote == -1)):
			correlation.append(1)
		elif (vdata.decision == "Abstain") and (mpvote == 0):
			correlation.append(0)	
		elif ((vdata.decision == "Yes") and (mpvote == -1)) or ((vdata.decision == "No") and (mpvote == 1)):
			correlation.append(-1)
		elif (vdata.decision == "Abstain") and (mpvote == 1 or mpvote == -1):
			correlation.append(0.5)	
		elif (vdata.decision == "Yes" or vdata.decision == "No") and (mpvote == 0):
			correlation.append(-0.5)	
		else:
			print "Error in parsing votes!"
			return 1

	root = tree.getroot()
	#mpname = root.find("FirstName").text + ' ' + root.find("LastName").text
	#mpname = root.find("Member").find("Name").text
	mpname = urlname
	plot.squareandhinton(correlation,mpname)


