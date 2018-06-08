#!/usr/bin/python
#needs pip qrcode, pip Pillow, pip lxml
# also do: npm install -g vanity-eth
import os
import sys
import json
import glob
import qrcode
import subprocess
from sys import exit
from time import sleep
import qrcode.image.svg

def stripKey(jsonAddr):
	key2=jsonAddr['privKey'][-10:]
	jsonAddr['privKey']=jsonAddr['privKey'][:-10]
	return key2

def padHEX(s):
        return s[2:].zfill(4)

def addrCreated():
	for fname in os.listdir('./'):
		if fname.startswith('VanityEth-log-'):
			return fname
	return False


vronAmnt = int(sys.argv[1])
os.system("vanityeth -l -i "+padHEX(hex(vronAmnt)))
count=0
addrFile = False
while addrFile == False and count<500:
	print "still waiting for file"
	addrFile = addrCreated()
	count+=1
	sleep(1)

fileroot='./'
jsonStr=""
with open(fileroot+addrFile) as f:
	jsonStr=f.readline()
jsonAddr=json.loads(jsonStr)
priv=jsonAddr['privKey']
print priv
priv=stripKey(jsonAddr)
print priv
print jsonAddr['privKey']

factory = qrcode.image.svg.SvgFillImage
addrWithKey = str(jsonAddr)
img = qrcode.make(addrWithKey, image_factory = factory)
img.save(str(priv)+".svg")
#test when finished with rest:
#os.remove(fileroot+addrFile)
