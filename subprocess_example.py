#! /usr/bin/env python3

""" subprocess example
it calls command lasting relatively long time,
than sleeps some time to show that command was running background,
than shows output until defined line and
than interrupts command and show the rest of output until command ends.
author: Ondrej Hejda
date: 31.3.2012

edit 1.4.2012 OH:
Timer from threading module used to interrupt """

from threading import Timer #interrupt timing
from time import sleep #sleep timing
import signal #interrupt signal name

import subprocess

cmd = ['ping','127.0.0.1','-c','10']
print('RUN: {} {} {} {}'.format(cmd[0],cmd[1],cmd[2],cmd[3]))

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

#setup and start interrupt timer
def stopit():
	p.send_signal(signal.SIGINT)
	print('INTERRUPT')
t = Timer(5,stopit)
t.start()

print('sleep 2s (to show its running on background)')
sleep(2)
print('BEGIN:')

#read output and show it
for line in p.stdout:
    print(line.decode('ascii').strip())
print('END')

p.communicate() #generate return code
print('RETURNS: {}'.format(p.returncode))