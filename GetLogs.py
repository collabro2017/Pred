import subprocess
import sys
import os
import time

def change_web_status(status):

    with open(status_file,'w') as f:
        f.write(status)
        
def getReversedLines(logs):
	logs_Lines = logs.splitlines()
	reversed_logs_lines = ""
	for i in reversed(logs_Lines):
		reversed_logs_lines += i + "\n"

	return (reversed_logs_lines)


logs = "\n\nStarting program. "

logs_file = "G:/Work/AI-EdenLLC/server/g0a_mvp_web-demo/logs.txt"


sleep_time = 2 # Sleep time in minutes.

max_n = 50 # Max number of logs evaluations that can be stored in the logs file.

status_file = "G:/Work/AI-EdenLLC/server/g0a_mvp_web-demo/status.txt"

if not os.path.exists(status_file):
	with open(status_file, 'w') as f:
		f.write("NO INITIATED")


while(True):

	isExc = False


	# Checks whether the file exists or is empty.
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

			old = f.read() # read everything in the file.

			# Remove log threads if they surpass the max_n of evaluations:
			if len(old.split('--------------------------------------------------------------------------------')) > max_n:
				old = '--------------------------------------------------------------------------------'.join(old.split('--------------------------------------------------------------------------------')[:max_n])
			
			f.seek(0)  # rewind.
			f.write(logs + old) # write the new line before.


	print(logs)
	
	change_web_status("Sleeping period")
	
	time.sleep(60*sleep_time) # Waiting sleep_time minutes between email checks.
	
