#!/bin/python
import json
import codecs
import sys
from datetime import datetime

tag_symbol = "#"

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print 'You need to pass a filename in argument. Ex: ./do2md.py Journal.json'
    sys.exit()

filename = sys.argv[1]

fp = open(filename)
all = json.load(fp)
#all is a dict [u'entries', u'metadata']
#metadata is not intersting (contains only a version number 1.0)

#all['entries'] is a list of dict.
#on entry is the following dict:
# [u'uuid', u'tags', u'text', u'richText', u'creationOSVersion',
# u'creationDeviceModel', u'creationDevice', u'modifiedDate',
# u'creationOSName', u'creationDeviceType', u'duration', u'timeZone',
# u'starred', u'creationDate', u'weather', u'location'

#entry2md is a function that will convert one single DayOne journal entry as
#a markdown file.
def entry2md(entry):
        date = datetime.strptime(entry['creationDate'],'%Y-%m-%dT%H:%M:%SZ')
	#date as the filename
        #it is assumed that there cannot be two entries in the same second.
        #If this is nevertheless the case, one of the two will be lost
        filename = date.strftime("%Y-%b-%d_%H-%m-%S")+".md"
        print filename
        #Add date as the title
        text = "# "+str(date)+"\n\n"+entry['text']
	#for some reason, "." and () are escaped
	text = text.replace("\.",".").replace("\(","(")\
                   .replace("\)",")").replace("\-","-")
	tags = ""
	#we add tags at the ends of each entry with the tag symbol
        #but only if the tag is not already in the text
	if 'tags' in entry.keys():
		for t in entry['tags']:
		    tag = " %s%s" %(tag_symbol,t)
                    if tag not in text:
                        tags += tag

	#we convert the dayone-moment photo link to local markdown link
        photos = dict()
	if 'photos' in entry.keys():
		for p in entry['photos']:
			#for each photos, we create a pair identifier/filename
                        #it looks that, sometimes, the photo was lost (no md5)
                        if 'md5' in p:
			    photos[p['identifier']] = "%s.%s" %(p['md5'],p['type'])
		for ph in photos:
			original = "![](dayone-moment://%s)" %ph
			new = "![](photos/%s)" %photos[ph]
			text = text.replace(original,new)
        #we add tags at the end of the text
	text += "\n\n%s" %tags
        #we add location
        if 'location' in entry.keys():
            location = entry['location']
            #print(location)
            place = "\n\n"
            for t in ['placeName','localityName','administrativeArea','country']:
                if t in location.keys():
                    place += location[t]+"\n"
            if 'longitude' in location.keys() and 'latitude' in location.keys():
                place += ""
                place += "long: "+str(location['longitude'])
                place += ", lat: "+str(location['latitude'])
            text += place
	fp = codecs.open(filename,'w','utf-8')
        fp.write(text)
        fp.close()

#i = 0
for entry in all['entries']:
#	print(i.keys())
#    print(i)
#    i+=1
#entry = all['entries'][90]
    entry2md(entry)
