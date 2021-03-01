#!/usr/bin/python

# sudo pip3 install websocket-server

# Example socket command text: "-f 118M:137M:20k -c 50% -g 50 -i 2s -1"

import subprocess
from websocket_server import WebsocketServer

def getpowerdata(rtlpstr):
    rtlp=["rtl_power"]+rtlpstr.split()
    header=[]
    samples=[]
    fstart=0
    fend=0
    fstep=0
    pout=subprocess.Popen(rtlp,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr=pout.communicate()
    p_status=pout.wait()
    stdout=stdout.decode('utf-8')
    firsttime=True
    for line in stdout.split("\n"):
        bits=line.strip().split(",")
        if len(bits)>=9:
            hzlow=float(bits[2])
            fend=float(bits[3])
            hzstep=float(bits[4])
            slen=int(bits[5])
            if firsttime==True:
                firsttime=False
                fstart=hzlow
                fstep=hzstep
            for c in range(6,len(bits)):
                frq=hzlow+(c-6)*hzstep
                sam=float(bits[c])
                samples.append(sam)
    header.append(fstart)
    header.append(fend)
    header.append(fstep)
    header.append(len(samples))
    return header+samples

def new_client(client,server):
    print("Client connected.")

def client_left(client,server):
    print("Client disconnected.")

def message_received(client,server,message):
    print("Client said: "+message)
    rtxt=""
    d=getpowerdata(message.strip())
    for v in d:
        rtxt+=str(round(v,4))+','
    rtxt+="END"
    server.send_message(client,rtxt)

PORT=43219
server=WebsocketServer(PORT,host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()

