import subprocess
import sys
import os
import time


def getReversedLines(logs):
	logs_Lines = logs.splitlines()
	reversed_logs_lines = ""
	for i in reversed(logs_Lines):
		reversed_logs_lines += i + "\n"

	return (reversed_logs_lines)


logs = "\n\nStarting program. "

logs_file = "G:/Work/AI-EdenLLC/server/g0a_mvp_web-demo/logs.txt"

while(True):

	isExc = False

	# Checks whether the file exists or is empty
	if not os.path.exists(logs_file) or os.stat(logs_file).st_size == 0:
		# try:
		logs += subprocess.run([sys.executable,'getEmails.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8','ignore')
		# except Exception as e:
			# logs += str(e)

		logs = getReversedLines(logs)

		with open(logs_file, "w") as f:
			f.write(logs)
	else:
		# try:
		logs = subprocess.run([sys.executable,'getEmails.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8','ignore')
		# except Exception as e:
		# logs = str(e)

		logs = getReversedLines(logs)

		# Prepending new log to file: 
		with open(logs_file, "r+") as f:
			old = f.read() # read everything in the file
			f.seek(0)  # rewind
			f.write(logs + old) # write the new line before

	print(logs)
		
	time.sleep((60*2)) # Waiting 2 min between email checks
	
