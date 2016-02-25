import os
import gzip
import urllib
 
# Following is the directory with log files,
# On Windows substitute it where you downloaded the files
root = "/home/mnigul/logs"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {}
urls = {}
users = {}
total = 0
 
for filename in os.listdir(root):
    if not filename.startswith("access.log"):
        print "Skipping unknown file:", filename
        continue
    if filename.endswith(".gz"):
        fh = gzip.open(os.path.join(root, filename))
    else:
        open(os.path.join(root, filename))
    print "Going to process:", filename
    for line in fh:
            total = total + 1
	    try:
		source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
		method, path, protocol = request.split(" ")
		_, status_code, content_lenght, _ =response.split(" ")
		content_lenght = int(content_lenght)
		path = urllib.unquote(path)
		if path.startswith("/~"):
			user, pask = path[2:].split("/",1)
			try:
				users[user] = users[user] + content_lenght
			except:
				users[user] = content_lenght
                url = "http://enos.itcollege.ee" + path
                try:
                        urls[url] = urls[url] + 1
                except:
                        urls[url] = 1
		for keyword in keywords:
		    if keyword in agent:
		        try:
		            d[keyword] = d[keyword] + 1
		        except KeyError:
		            d[keyword] = 1
		        break # Stop searching for other keywords
	    except ValueError:
		pass # This will do nothing, needed due to syntax

print "Total lines:", total
 
results = d.items()
results.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in results:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"

results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for url, hits in results[:5]:
    print url, "==>", hits, "(", hits * 100 / total, "%)"

results = users.items()
results.sort(key = lambda item:item[1], reverse=True)
for user, transfered_bytes in results[:5]:
    print user, "==>", transfered_bytes / (1024 * 1024), "MB"












