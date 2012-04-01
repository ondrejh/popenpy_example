#! /usr/bin/env python3

""" subprocess example
it calls command lasting relatively long time,
than sleeps some time to show that command was running background,
than shows output until defined line and
than interrupts command and show the rest of output until command ends.
author: Ondrej Hejda
date: 31.3.2012 """


from time import sleep

import signal

import subprocess

cmd = ['ping','127.0.0.1','-c','10']
print('run: ping 127.0.0.1 -c 10')

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

print('sleep 2s (to show its running on background)')
sleep(2)
cnt = 0
print('BEGIN:')
for line in p.stdout:
    print(line.decode('ascii').strip())
    cnt+=1
    if cnt==6: #stop (interrupt) it on line 6
        p.send_signal(signal.SIGINT)
        print('INTERRUPT')
print('END')
p.communicate() #generate return code
print('RETURNS: {}'.format(p.returncode))
