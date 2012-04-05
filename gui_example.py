#! /usr/bin/env python3

from tkinter import *
from threading import Thread
import signal #interrupt signal name
import subprocess

#command thread
class thrCmd(Thread):
	def __init__ (self,cmd,txt):
		Thread.__init__(self)
		self.cmd = cmd
		self.txt = txt
	def run(self):
		self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
		#read output and show it
		for line in self.p.stdout:
			self.txt.insert(END,line.decode('ascii').strip())
			self.txt.insert(END,'\n')
	def join(self):
		self.p.send_signal(signal.SIGINT)

#application class
class runapp_gui(Frame):
	''' gui for executing terminal application '''
	
	def __init__(self,master=None):
		self.root = Tk()
		Frame.__init__(self,master)
		self.createWidgets()
	
	def createWidgets(self):
		#button frame and buttons
		self.frmButtons = Frame(self.root)
		self.frmButtons.pack(fill=X)
		self.btnRun = Button(self.frmButtons,text='RUN',command=self.btnRunClick)
		self.btnRun.pack(side=LEFT)
		self.btnStop = Button(self.frmButtons,text='STOP',command=self.btnStopClick)
		self.btnStop.pack(side=LEFT)
		#command frame entry
		self.frmEntry = Frame(self.root)
		self.frmEntry.pack(fill=X)
		Label(self.frmEntry,text='Command:').pack(side=LEFT)
		self.strCommand = StringVar()
		self.entCmd = Entry(self.frmEntry,textvariable=self.strCommand)
		self.entCmd.pack(side=LEFT)
		self.strCommand.set('ping 127.0.0.1')
		#text output
		self.txtOutput = Text()
		self.txtOutput.pack(fill=BOTH,expand=1)
		
	def btnRunClick(self):
		self.txtOutput.insert(END,'RUN: ')
		self.txtOutput.insert(END,self.strCommand.get())
		self.txtOutput.insert(END,'\n')
		self.app = thrCmd(self.strCommand.get().split(),self.txtOutput)
		self.app.start()
		pass
		
	def btnStopClick(self):
		self.app.join()
		self.txtOutput.insert(END,'STOP\n')
		pass
		
#run application
app = runapp_gui()
app.mainloop()
