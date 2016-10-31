import json 
f = open('json.txt', 'r')
a = json.load(f)
#print a
#print type(a)
for i in a[u'results']:
    print "name-%s address-%s" %  (i['name'], i['formatted_address'])

