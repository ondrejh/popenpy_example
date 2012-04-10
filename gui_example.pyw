#! /usr/bin/env python3

from tkinter import *
from threading import Thread
import signal #interrupt signal name
import subprocess
import os

def myread(what):
	what.flush()
	return what.readline()

#command thread
class thrCmd(Thread):
	def __init__ (self,cmd,out):
		Thread.__init__(self)
		self.cmd = cmd
		self.out = out
	def run(self):
		if os.name=='nt':
			self.p = subprocess.Popen(self.cmd,
						  #shell=False,
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE,
						  stderr=subprocess.STDOUT,
						  #close_fds=True,
						  bufsize=0,
						  creationflags=0x8000000)# CREATE_NO_WINDOW = 0x8000000
		else:
			self.p = subprocess.Popen(self.cmd,
						  #shell=False,
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE,
						  stderr=subprocess.STDOUT,
						  bufsize=0)#,
						  #close_fds=True)#,
						  #creationflags=0x8000000)# CREATE_NO_WINDOW = 0x8000000
						  
		#read output and show it
		while self.p.poll()==None:
			try:
				self.out(self.p.stdout.read(1))
			except:
				pass
                #for line in myread(self.p.stdout):
		#	try:
		#		self.out('{}\n'.format(line.decode('ascii').strip()))
		#	except:
		#		pass
	def join(self):
		try:
			self.p.terminate()
		except:
			pass
		#self.p.send_signal(signal.SIGINT)
			
	def retCode(self):
		try:
			self.p.wait()
			return self.p.returncode
		except:
			return None
			
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
		if os.name == 'nt':
			self.strCommand.set('testapp/testapp.exe')
			#self.strCommand.set('ping 127.0.0.1 -t')
		else:
			self.strCommand.set('./testapp/testapp.run')
			#self.strCommand.set('ping 127.0.0.1')
		#text output
		self.txtOutput = Text(background='black',
				      foreground='green',
				      font='Courier 10')
		self.txtOutput.pack(fill=BOTH,expand=1)
		#print(self.txtOutput.config('font'))
		
	def btnRunClick(self):
		self.printOut('\n\nRUN: {}\n'.format(self.strCommand.get()))
		self.app = thrCmd(self.strCommand.get().split(),self.printOut)
		self.app.start()
		pass
		
	def btnStopClick(self):
		self.app.join()
		self.printOut('\nRETURN: {}'.format(self.app.retCode()))
		#self.txtOutput.insert(END,'\nRETURN: {}\n'.format(self.app.retCode()))
		pass

	def printOut(self,txt):
		self.txtOutput.insert(END,txt)
		self.txtOutput.see(END)
		
#run application
app = runapp_gui()
app.mainloop()
