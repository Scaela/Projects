import os
from ftplib import FTP

def moveFTPFiles(serverName,userName,passWord,remotePath,localPath,deleteRemoteFiles=False,onlyDiff=False):
	"""Connect to an FTP server and bring down files to a local directory"""
	try:
		ftp = FTP(serverName)
	except:
		print ("Couldn't find server")
	ftp.login(userName,passWord)
	ftp.cwd(remotePath)
	
	try:
		print ("Connecting...")
		if onlyDiff:
			print(localDirectoryPath,remoteDirectoryPath)
			lFileSet = set(os.listdir(localDirectoryPath))
			rFileSet = set(ftp.nlst())
			
			transferList = list(rFileSet - lFileSet)
			print ("Missing: " + str(len(transferList)))
		else:
			transferList = ftp.nlst()
			#print(transferList)
		delMsg = ""	
		filesMoved = 0
		for fl in transferList:
			# create a full local filepath
			localFile = localPath + fl
			grabFile = True
			if grabFile:				
				#open a the local file
				fileObj = open(localFile, 'wb')
				# Download the file a chunk at a time using RETR
				ftp.retrbinary('RETR ' + fl, fileObj.write)
				# Close the file
				fileObj.close()
				filesMoved += 1
				
			# Delete the remote file if requested
			if deleteRemoteFiles:
				ftp.delete(fl)
				delMsg = " and Deleted"
			
		print ("Files Moved" + delMsg + ": " + str(filesMoved) + " on " + timeStamp())
	except:
		print ("Connection Error - " + timeStamp())
	ftp.close() # Close FTP connection
	ftp = None

def timeStamp():
    """returns a formatted current time/date"""
    import time
    return str(time.strftime("%a %d %b %Y %I:%M:%S %p"))

if __name__ == '__main__':
	#--- constant connection values
	ftpServerName = "172.1.254.125"
	#ftpU = "ftpusername"
	ftpU = "opmstools"
	ftpP = "$opms$123"
	remoteDirectoryPath = "/Rocia"
	localDirectoryPath = """home/rocia/Desktop/FTP"""
	
	print ("\n-- Retreiving Files----\n")
	
	deleteAfterCopy = False 	#set to true if you want to clean out the remote directory
	onlyNewFiles = True	#set to true to grab & overwrite all files locally
	moveFTPFiles(ftpServerName,ftpU,ftpP,remoteDirectoryPath,localDirectoryPath,deleteAfterCopy,onlyNewFiles)
