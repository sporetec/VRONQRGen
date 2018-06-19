#!/usr/bin/python
#needs pip qrcode, pip Pillow, pip lxml
# also do: npm install -g vanity-eth
#and apt-get install libmagickwand-dev, pip install Wand
import os
import sys
import json
import glob
import qrcode
import subprocess
from sys import exit
from time import sleep
import qrcode.image.svg
from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

#this function removes the last 10 chars from the given address json variable privatekey and returns it
def stripKey(jsonAddr):
	key2=jsonAddr['privKey'][-10:]
	jsonAddr['privKey']=jsonAddr['privKey'][:-10]
	return key2

#this function fills the given string with zeros to be always 4 chars long, if 4 chars does nothing
def padHEX(s):
        return s[2:].zfill(4)

#this function checks if the creating of the address is done by checking if a file exists
def addrCreated():
	for fname in os.listdir('./'):
		if fname.startswith('VanityEth-log-'):
			return fname
	return False
#set arg to vron ammount
vronAmnt = int(sys.argv[1])
#create vanity address starting with vron ammount in hex
#os.system("vanityeth -l -i "+padHEX(hex(vronAmnt)))
count=0
addrFile = False
#wait for address to be genearted by checking for log file
while addrFile == False and count<500:
	print "still waiting for file"
	addrFile = addrCreated()
	count+=1
	sleep(1)

#create json variable from generated file
fileroot='./'
jsonStr=""
with open(fileroot+addrFile) as f:
	jsonStr=f.readline()
jsonAddr=json.loads(jsonStr)
#strip last 10 chars from the key
priv=stripKey(jsonAddr)
print priv
print jsonAddr['privKey']

#qr code presets
factory = qrcode.image.svg.SvgFillImage
addrWithKey = str(jsonAddr)
img = qrcode.make(addrWithKey, image_factory = factory)
img.save(str(priv)+".svg")
#os.remove(fileroot+addrFile)

#draw qrcode and privatekey parts on the bill
bill=str(vronAmnt)+"V.png"
qrcode = Image(filename=str(priv)+'.svg')
with Image(filename=bill) as canvas:
	with Drawing() as context:
		context.font = 'wandtests/assets/League_Gothic.otf'
		context.font_size = 40
		context.fill_color = Color('white')
		context.text((canvas.width / 2)-(canvas.width / 4), (canvas.height / 2)-(canvas.height / 4), priv)
		context.composite(operator='replace', left=10, top=10, width=15, height=15, image=qrcode)
		context(canvas)
	canvas.save(filename='bill.png')

