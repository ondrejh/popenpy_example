#! /usr/bin/env python3

""" subprocess example
it calls command lasting relatively long time,
shows output and than interrupts it
and show the rest of output until command ends.
author: Ondrej Hejda
date: 31.3.2012

edit 1.4.2012 OH:
Timer from threading module used to interrupt
edit 3.4.2012 OH:
W32 testing, CREATE_NO_WINDOW flag, signal, ect.
edit 4.4.2012 OH:
findout if it's run on windows or not and change some details """

from threading import Timer #interrupt timing
from time import sleep #sleep timing
import signal #interrupt signal name

import os
import subprocess

#find out if running windows system
widle = False
if os.name=='nt':
        widle = True

#command to run
#ping ... good example, except it differs in windows .. ugh!
cmd = ['ping','127.0.0.1']
if widle:
        cmd.append('-t')
print('RUN:',cmd[0],cmd[1])

#run it (also os dependent)
if widle: # on windows
	p = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
						stderr=subprocess.STDOUT,#, close_fds=True)
						creationflags=0x8000000)# CREATE_NO_WINDOW = 0x8000000
else: #on linux
	p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
						stderr=subprocess.STDOUT, close_fds=True)

#setup and start interrupt timer
def stopit():
        #print('TIMER')
        if p.poll()==None:
                '''if wok:
			#as windows don't have sigint but ctrl_c_event but it doesn't work same as keystroke .. ugh! again
                        #p.send_signal(signal.CTRL_C_EVENT)
                        #p.send_signal(signal.CTRL_BREAK_EVENT)
                        #p.kill()
                        p.terminate()
                else:
			#sigint .. works as ctrl-c keystroke
                        p.send_signal(signal.SIGINT)'''
                p.terminate()
                #print('INTERRUPT')
t = Timer(4.75,stopit)
t.start()

'''#sleep a while
print('sleep 2s (to show its running on background)')
sleep(2)'''
print('BEGIN:')

#read output and show it
for line in p.stdout:
    print(line.decode('ascii').strip())
print('END')

p.communicate() #generate return code
print('RETURNS: {}'.format(p.returncode))

#stop timer (if started)
t.cancel()
