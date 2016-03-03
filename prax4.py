import argparse
import os
import urllib
import GeoIP

gi = GeoIP.open("GeoIP.dat", GeoIP.GEOIP_MEMORY_CACHE)

parser = argparse.ArgumentParser(description='Apache2 log parser.')
parser.add_argument('--path',
    help="Path to Apache2 log files", default="/var/log/apache2")
parser.add_argument('--top-urls',
    help="Find top URL-s", action='store_true')
parser.add_argument('--geoip',
    help="Resolve IP-s to country codes", default ="usr/share/GeoIP/GeoIP.dat")
parser.add_argument('--verbose',
    help="Increase verbosity", action="store_true")
args = parser.parse_args()

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} 
urls = {}
user_bytes = {}
countries = {}
ip_addresses = {}


total = 0
import gzip
for filename in os.listdir(args.path):
    if not filename.startswith("access.log"):
        continue
    if filename.endswith(".gz"):
	continue #skip compresssed files
        fh = gzip.open(os.path.join(args.path, filename))
    else:
        fh = open(os.path.join(args.path, filename))
    if args.verbose:
        print "Parsing:", filename
    for line in fh:
        total = total + 1
        try:
            source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
            method, path, protocol = request.split(" ")
        except ValueError:
            continue # Skip garbage
	
	#TODAY
	source_ip, _, _, timestamp = source_timestamp.split(" ", 3)
	
	if not ":" in source_ip: #skip IPv6
		ip_addresses[source_ip] = ip_addresses.get(source_ip, 0) + 1
	cc = gi.country_code_by_addr(source_ip)
#	print source_ip, "resolves to", cc
	countries[cc] = countries.get(cc, 0) + 1

	ip_addresses[source_ip] = ip_addresses.get(source_ip, 0) + 1

	#BREAK
            
        if path == "*": continue # Skip asterisk for path

        _, status_code, content_length, _ = response.split(" ")
        content_length = int(content_length)
        path = urllib.unquote(path)
        
        if path.startswith("/~"):
            username = path[2:].split("/")[0]
            try:
                user_bytes[username] = user_bytes[username] + content_length
            except:
                user_bytes[username] = content_length

        try:
            urls[path] = urls[path] + 1
        except:
            urls[path] = 1
        
        for keyword in keywords:
            if keyword in agent:
                try:
                    d[keyword] = d[keyword] + 1
                except KeyError:
                    d[keyword] = 1
                break

def humanize(bytes):
    if bytes < 1024:
        return "%d B" % bytes
    elif bytes < 1024 ** 2:
        return "%.1f kB" % (bytes / 1024.0)
    elif bytes < 1024 ** 3:
        return "%.1f MB" % (bytes / 1024.0 ** 2)
    else:
        return "%.1f GB" % (bytes / 1024.0 ** 3)

from lxml import etree
from lxml.cssselect import CSSSelector
 
document =  etree.parse(open('BlankMap-World6.svg'))

for country_code, hits in countries.items():
	sel = CSSSelector("#" + country_code)
	for j in sel(document):
   	 j.set("style", "fill:red")
    	# Remove styling from children
    	for i in j.iterfind("{http://www.w3.org/2000/svg}path"):
      	  i.attrib.pop("class", "")
 
	with open("highlighted.svg", "w") as fh:
   	 fh.write(etree.tostring(document))    

print
print("Top IP-addresses:")
results = ip_addresses.items()
results.sort(key = lambda item:item[1], reverse=True)
for source_ip, hits in results[:5]:
    print source_ip, "==>", hits

print
print("Top 5 bandwidth hoggers:")
results = user_bytes.items()
results.sort(key = lambda item:item[1], reverse=True)
for user, transferred_bytes in results[:5]:
    print user, "==>", humanize(transferred_bytes)
    
print
print("Top 5 visited URL-s:")
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for path, hits in results[:5]:
    print "http://enos.itcollege.ee" + path, "==>", hits, "(", hits * 100 / total, "%)"

total = 0









