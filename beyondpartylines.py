import app.gui.gui
import Tkinter
import ttk


def helpme():
	helppopup = Tkinter.Toplevel()

	helpstring = "How to use this application: \n a) Clicking \'download\' will download the most recent votes that have gone through the Canadian House of Commons. \n b) Clicking on any of the votes will enable you to vote or to access more information. Press \'Bill details\' to be redirected to a webpage with more information about the bill and the vote. \n Press \'Vote results\' to see the votes of any of the MPs in parliament. Press \'Vote Yes\' or \'Vote No\' to register your vote on that issue. \'Abstain\' to avoid having to vote on the issue. Double \n click on any vote to see a short summary. \n c) To compare your votes with a member of parliament, click \'Compare\'. In the popup, type the name of the MP you would like to compare your votes with. The graph that appears is \n a Hinton graph. A large black box means you disagreed, while a large white box means you agreed on an issue. If both of you abstained, the square will be grey. If you abstained and \n the other person voted, the square will be smaller and white, while if the other person abstained and you voted, the square will be small and black. The percentage given is my \n calculation of how much you agreed with the MP."

	helplabel = ttk.Label(helppopup, text=helpstring, background="white")
	helplabel.grid(row=0,column=0,columnspan=5)

def credit():
	creditpopup = Tkinter.Toplevel()

	creditstring = "This application is distributed under a Creative Commons BY-NC-SA 3.0 license. \nSee http://wbrenna.uwaterloo.ca for details. \n \nDeep thanks to Michael at openparliament.ca for providing a clean interface to see parliamentary decisions, \nand parl.gc.ca for providing transparent XML data."

	creditlabel = ttk.Label(creditpopup, text=creditstring, background="white")
	creditlabel.grid(row=0,column=0,columnspan=5)


if __name__ == '__main__':
	root = Tkinter.Tk()
	root.title("BeyondPartyLines")

	menubar = Tkinter.Menu(root)
	filemenu = Tkinter.Menu(menubar, tearoff=0)
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	filemenu2 = Tkinter.Menu(menubar, tearoff=0)
	filemenu2.add_command(label="Credits", command=credit)
	filemenu2.add_separator()
	filemenu2.add_command(label="Help", command=helpme)
	
	menubar.add_cascade(label="Help", menu=filemenu2)


	root.config(menu=menubar)

	widget = app.gui.gui.voteGui(root)
	root.mainloop()
