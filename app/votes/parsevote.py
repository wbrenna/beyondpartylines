import parliamentdatastructs
#import fileinput
import os
import re

def sort_file(filename):
	filehandl = open(filename,"r")
	lines=[] # give lines variable a type of list
	while 1:
		line = filehandl.readline()
		if not line:
			break
		lines.append(line.rstrip())
	lines.sort(reverse=True)
	filehandl.close()
	filehandl = open(filename,"w")
	for line in lines: 
#Make sure we aren't spitting blanks back into the file
		if not(line == ""):
			filehandl.write(line)
			filehandl.write("\n")
	filehandl.close()
		
	

def returnvotes(votearray,datadir):
#Here we spit out all of the votes sequentially.
	filelist = os.listdir(datadir)
	filelist.sort()
	#print filelist[1]
	numfiles = len(filelist)
	#global votearray = list()

	for name in filelist:
		tmp = parliamentdatastructs.votedata()
		votefile = open(datadir+name,"r")
		tmp2 = re.split('_',name)
		tmp.ses = tmp2[1]
		tmp.parl = tmp2[0]
		tmp.vote = votefile.readline().rstrip()
		tmp.bill = votefile.readline().rstrip()
		tmp.title = votefile.readline().rstrip()
		tmp.decision = votefile.readline().rstrip()
		while True:
			line = votefile.readline().rstrip()
			if not line:
				line = votefile.readline()
				if not line:
					break
				elif len(line) > 70:
					tmp.description += line[0:70]
					for i in range(70, len(line), 70):
						tmp.description += '-\n' + line[i:i+70] 
				else:
					tmp.description += line	
			else:
				tmp.description += line 
		votefile.close()
		votearray.append(tmp)		


def writevote(votedata,vote,datadir,votename):
	if vote is not "NA":
		print "Vote of \'" + vote + "\' recorded for vote number " + str(votedata.vote) + "."

		filename = datadir + str(votedata.parl) + '_' + str(votedata.ses) + '_' + str(votedata.vote) + '.txt'


		try:
			datafile = open(filename,"r")
		except Exception, e:
			print "Problem opening file!"
			print e
			return 0


		votefile = open(votename,"a")

		bill = datafile.readline()
		title = datafile.readline()
		decision = datafile.readline()
		description = datafile.readline()
		datafile.close()

		myvotedata = str(votedata.parl) + " " + str(votedata.ses) + " " + str(votedata.vote) + " " + str(vote)
		votefile.write(myvotedata + "\n")
		votefile.close()

		sort_file(votename)

#And we remove the file from our parsing directory
		os.remove(filename)
	else:
		print "Null vote detected...not recorded."


