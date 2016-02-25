fh = open("Downloads/access.log")
win = 0 #create integer variable and name it "win"
total = 0 #create another integer variable

for line in fh:
	total = total + 1
	try:
		source_timestamp, request, response, _, _, agent, _ = line.split("\"")
		method, path, protocol = request.split(" ")
#		print("User visited URL: http://enos.itcollege.ee" + path)
		
		if "Windows" in agent:
			win = win + 1
	
	except ValueError:
		pass #does nothing, needed for syntax
		print("Failed to parse:", line)
	

print "Total requests:", total
print "Requests form Windows:", win
print "Windows persentage:", win * 100 / total, "%"
print "Windows persentage: %.02f%%" % (win * 100 / total)

