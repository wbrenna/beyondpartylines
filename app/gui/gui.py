import Tkinter
import ttk
#import Pmw
import webbrowser
from app.votes import parliamentdatastructs,parsevote,grabrecent
from app.names import names
import platform
import os
import tkMessageBox
import copy

#Make sure the directory structure is setup properly
if platform.system() == 'Windows':
	datadir = 'app\\db\\'
else:
	datadir = 'app/db/'

if not os.path.exists(datadir):
	os.makedirs(datadir)

cursitting = 'currentsitting.dat'
currentsitting = parliamentdatastructs.currentsessionofparliament()
checksitting = parliamentdatastructs.currentsessionofparliament()


class voteGui():
	def get_list(self,event):
		"""
		function to read the listbox selection
		and put the result in an entry widget
		"""
		# get selected line index
		index = self.listbox.curselection()[0]
		# get the line's text
		seltext = self.listbox.get(index)
		# delete previous text in entrybar
		self.entrybar.delete(0, 50)
		# now display the selected text
		self.entrybar.insert(0, seltext)

	def download_new(self):
		"""
		This function downloads the new votes automatically.
		"""
		if(grabrecent.getcurrentsitting(cursitting,currentsitting,checksitting)):
#Now grab the votes and download them
			grabrecent.go(cursitting,datadir,currentsitting)
			self.refresh_list()
		else:
#Check to see a delay - if so, popup and ask
			#print checksitting.last
			#print currentsitting.last
			self.popupsittingchoice()
			#grabrecent.go(cursitting,datadir,newsitting)
			#self.refresh_list()


	def refresh_list(self):
		"""
		Refresh the list of possible votes
		"""
		listarr = []
		parsevote.returnvotes(listarr,datadir)
		self.listbox.delete(0, Tkinter.END)
		#print listarr[1].vote

		for item in listarr:
			if item.bill is "":
				item.bill = "N/A"
			self.listbox.insert(Tkinter.END, item.vote+" - Bill "+item.bill)
		
#This might be deprecated...
	def sort_list(self):
		"""
		function to sort listbox items case insensitive
		"""
		temp_list = list(self.listbox.get(0, Tkinter.END))
		temp_list.sort(key=str.lower)
		# delete contents of present listbox
		self.listbox.delete(0, Tkinter.END)
		    # load listbox with sorted data
		for item in temp_list:
			self.listbox.insert(Tkinter.END, item)
	
	def launchBill(self):
		index = int(self.listbox.curselection()[0])
		votearr = []
		parsevote.returnvotes(votearr,datadir)
		url = "http://www2.parl.gc.ca/HouseChamberBusiness/Chambervotedetail.aspx?Language=E&Mode=1&Parl=%(parliamentnum)s&Ses=%(sessnum)s&FltrParl=%(parliamentnum)s&FltrSes=%(sessnum)s&vote=%(votenum)s" % {'parliamentnum' : votearr[index].parl, 'sessnum' : votearr[index].ses, 'votenum' : votearr[index].vote}
		webbrowser.open_new_tab(url)


	def launchVotes(self):
		index = int(self.listbox.curselection()[0])
		votearr = []
		parsevote.returnvotes(votearr,datadir)
		url = "http://openparliament.ca/bills/votes/%(parliamentnum)s-%(sessnum)s/%(votenum)s/" % {'parliamentnum' : votearr[index].parl, 'sessnum' : votearr[index].ses, 'votenum' : votearr[index].vote}
		webbrowser.open_new_tab(url)


	def vote(self,myvote):
		votename = 'votes.dat'

		try:
#Need to catch exceptions here! Otherwise it will call parsevote.writevote with a bad index and KILL EVERYTHING
			index = int(self.listbox.curselection()[0])
#Use this index to pick out which of the sessions we're in
			votearr = []
			parsevote.returnvotes(votearr,datadir)
			parsevote.writevote(votearr[index],myvote,datadir,votename)
		except IndexError:
			pass

		self.refresh_list()


	def infopopup(self,event):
		index = int(self.listbox.curselection()[0])
		votearr = []
		parsevote.returnvotes(votearr,datadir)
		text1 = votearr[index].parl + '-' + votearr[index].ses + ' ' + votearr[index].vote + '\n'
		text2 = 'Title: ' + votearr[index].bill + ' ' + votearr[index].title + '\n'
		text3 = 'Description: ' + votearr[index].description + '\n'
		text4 = 'Decision: ' + votearr[index].decision

		self.mylabel.configure(text=text1+text2+text3+text4)
		self.top.geometry('+%d+%d' %(self.listbox.winfo_rootx()+50,self.listbox.winfo_rooty()-50))
		self.top.deiconify()


	def hidepopup(self,event):
		self.top.withdraw()

	def runcomp(self, event):
		mpname = self.popup.entry.get()
		key = names.searchforkey(mpname)
		names.plotvotes(key)

	def runcomp2(self):
		mpname = self.popup.entry.get()
		key = names.searchforkey(mpname)
		names.plotvotes(key)


	def comparevote(self):
		self.popup = Tkinter.Toplevel()
		self.popup.entry = ttk.Entry(self.popup, width=40, background="white")
		self.popup.entry.insert(0, 'Enter a politician to compare your votes')
		self.popup.entry.grid(row=1, column=0, columnspan=3)
		self.popup.abutton1 = ttk.Button(self.popup, text='Compare', command=self.runcomp2)
		self.popup.abutton1.grid(row=2, column=0, sticky=Tkinter.W)
		self.popup.abutton2 = ttk.Button(self.popup, text='Cancel', command=self.popup.destroy)
		self.popup.abutton2.grid(row=2, column=1, sticky=Tkinter.W)
		self.popup.entry.bind('<Return>', self.runcomp)

	def popupusecurrent(self):
		#newsitting = currentsitting
		grabrecent.go(cursitting,datadir,currentsitting)
		#print currentsitting.last
		self.refresh_list()
		#self.popup.destroy()

	def popupusechosen(self):
		grabrecent.go(cursitting,datadir,checksitting)
		#print checksitting.last
		self.refresh_list()
		#self.popup.destroy()

	def popupsittingchoice(self):
		#self.popup = Tkinter.Toplevel()
		#self.popup.transient(parent=self)
		#self.popup.desc = ttk.Label(self.popup, text="It has been a while since updating. \nSelect either the most recent sitting (\"Current\") or \n download all (\"All\").")
		#self.popup.desc.grid(row=0,columnspan=4)
		#self.popup.abutton1 = ttk.Button(self.popup, text='All', command=self.popupusechosen)
		#self.popup.abutton1.grid(row=2, column=0, sticky=Tkinter.W)
		#self.popup.abutton2 = ttk.Button(self.popup, text='Current', command=self.popupusecurrent)
		#self.popup.abutton2.grid(row=2, column=1, sticky=Tkinter.W)

		answer = tkMessageBox.askyesno("Stale Database", "It has been a while since updating. Jump to the most recent sitting (\"Yes\")? Otherwise we will download all votes since last time (\"No\").")
		if (answer):
			self.popupusecurrent()
		else:
			self.popupusechosen()

		#self.popup.entry1.bind('<Return>', self.popupusecurrent)
		#self.popup.entry2.bind('<Return>', self.popupusecurrent)
		#self.popup.entry3.bind('<Return>', self.popupusecurrent)


	def __init__(self,parent):

		self.listbox = Tkinter.Listbox(parent, width=50, height=6)
		self.listbox.grid(row=0, column=0, columnspan=5)

		 
		yscroll = ttk.Scrollbar(command=self.listbox.yview, orient=Tkinter.VERTICAL)
		yscroll.grid(row=0, column=5, sticky=Tkinter.N+Tkinter.S)
		self.listbox.configure(yscrollcommand=yscroll.set)
		 
		self.entrybar = ttk.Entry(parent, width=40, background="white")
		self.entrybar.insert(0, 'Click on an item in the listbox')
		self.entrybar.grid(row=1, column=0, columnspan=5)

# load the listbox with data
		self.refresh_list()


		button3 = ttk.Button(parent, text='Vote Yes', command=lambda: self.vote("Yes"))
		button3.grid(row=2, column=0, sticky=Tkinter.W)

		button4 = ttk.Button(parent, text='Vote No', command=lambda: self.vote("No"))
		button4.grid(row=3, column=0, sticky=Tkinter.W)

		button7 = ttk.Button(parent, text='Abstain', command=lambda: self.vote("Abstain"))
		button7.grid(row=3, column=1)

		button1 = ttk.Button(parent, text='Compare', command=self.comparevote)
		button1.grid(row=2, column=1)

		button5 = ttk.Button(parent, text='Bill details', command=self.launchBill)
		button5.grid(row=2, column=2)

		button6 = ttk.Button(parent, text='Vote results', command=self.launchVotes)
		button6.grid(row=3, column=2)

		button8 = ttk.Button(parent, text='Quit', command=parent.destroy)
		button8.grid(row=3, column=4, sticky=Tkinter.E)

		button9 = ttk.Button(parent, text='Download', command=self.download_new)
		button9.grid(row=2, column=4, sticky=Tkinter.E)



#create the hover box
		self.top = Tkinter.Toplevel()
		self.top.wm_overrideredirect(boolean=True)
		self.mylabel = ttk.Label(self.top, text="Initially blank")
		self.mylabel.grid(row=0,column=0,columnspan=5)
		self.listbox.update_idletasks()
		self.top.update_idletasks()
		self.top.withdraw()



#and the bindings...
		self.listbox.bind('<ButtonRelease-1>', self.get_list)
		self.listbox.bind('<Double-Button-1>', self.infopopup)
		self.listbox.bind('<Button-1>',self.hidepopup)
		self.top.bind('<Button-1>',self.hidepopup)


def OpenFileDialog():
	print "open"

