import argparse
import os
import urllib
import GeoIP

#print env.get_template("report.html").render(variable="blah")


gi = GeoIP.open("GeoIP.dat", GeoIP.GEOIP_MEMORY_CACHE)

parser = argparse.ArgumentParser(description='Apache2 log parser.')
parser.add_argument('--path',
    help="Path to Apache2 log files", default="/var/log/apache2")
parser.add_argument('--top-urls',
    help="Find top URL-s", action='store_true')
parser.add_argument('--geoip',
    help="Resolve IP-s to country codes", default ="/usr/share/GeoIP/GeoIP.dat")
parser.add_argument('--verbose',
    help="Increase verbosity", action="store_true")
args = parser.parse_args()

try:
	gi = GeoIP.open(args.geoip, GeoIP.GEOIP_MEMORY_CACHE)
except:
	print "Failed to open up GeoIP database, are you sure %s exists?" % args.geoip
	exit(255)

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
    elif bytes < 1024 ** 4:
        return "%.1f GB" % (bytes / 1024.0 ** 3)
    else:
        return "%.1f TB" % (bytes / 1024.0 ** 4)

from lxml import etree
from lxml.cssselect import CSSSelector
 
document =  etree.parse(open('BlankMap-World6.svg'))

max_hits = max(countries.values())
print("country with max amount of hits:", max_hits)

for country_code, hits in countries.items():
	if not country_code: continue #skip localhost
	print country_code, hex(hits * 255 / max_hits)[2:] #2: skips 0x of hexadecimal numbers
	sel = CSSSelector("#" + country_code.lower())
	for j in sel(document):
	#This will make the tones of red different based on nr of hits
   		#j.set("style", "fill:#" + hex(hits * 255 /max_hits)[2:] + "0000")
		#120 dgr is green, 0 is red, 0 to max hits will be coloured green to red
		j.set("style", "fill:hsl(%d, 60%%, 70%%);" % (120 - hits * 120 / max_hits))
    	# Remove styling from children
    	for i in j.iterfind("{http://www.w3.org/2000/svg}path"):
      		i.attrib.pop("class", "")
 
with open("highlighted.svg", "w") as fh:
	fh.write(etree.tostring(document))    

from jinja2 import Environment, FileSystemLoader #this is the template engine we will use

env = Environment(
	loader=FileSystemLoader(os.path.dirname(__file__)),
	trim_blocks=True)

#user_bytes = sorted(user_bytes.items(), key = lambda item:item[1], reverse =True)

import codecs
with codecs.open("output.html", "w", encoding ="utf-8") as fh:
	fh.write(env.get_template("report.html").render(
		humanize = humanize, # this is the templating the engine will use
		url_hits = sorted(urls.items(), key=lambda i:i[1], reverse=True),
		user_bytes = sorted(user_bytes.items(), key = lambda item:item[1], reverse=True),
		some_other_variable = "This is now also accessible from template"
	))

	# A more convenient way is: env.get_template("...").render(locals())
	# locals() is a dict which contains all locally defined variables

#os.system("x-www-browser file://" + os.path.realpath("output.html") + " &")

print
print("Top IP-addresses:")
results = ip_addresses.items()
results.sort(key = lambda item:item[1], reverse=True)
for source_ip, hits in results[:5]:
    print source_ip, "==>", hits

print
print("Top 5 bandwidth hoggers:")
for user, transferred_bytes in results[:5]:
    print user, "==>", humanize(transferred_bytes)
    
print
print("Top 5 visited URL-s:")
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for path, hits in results[:5]:
    print "http://enos.itcollege.ee" + path, "==>", hits, "(", hits * 100 / total, "%)"

total = 0









