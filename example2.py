import os
from datetime import datetime

def humanize(bytes):
	if bytes < 1024:
		return "%d B" % bytes
	elif bytes < 1024 ** 2: 
		return "%.1f kB" % (bytes / 1024)
	elif bytes < 1024 ** 3:
		return "%.1f MB" % (bytes / 1024 ** 2)
	elif bytes < 1024 ** 4:
		return "%.1f GB" % (bytes / 1024 ** 3)
	else:
		return "%.1f TB" % (bytes / 1024.0 ** 4)

files = []

for filename in os.listdir("."):
	mode, inode, device, nlink, uid, gid, size, atime, mtime, ctime = os.stat(filename)
	files.append((filename, datetime.fromtimestamp(mtime), size))

files.sort(key = lambda(filename, dt, size):dt)

for filename, dt, size in files:
	print filename, dt, humanize(size)

print "Newest file is:", files[-1][0]
print "Oldest file is:", files[0][0]


	#print filename, humanize(size),datetime.fromtimestamp(mtime)
