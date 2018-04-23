#-*-coding:utf-8-*-


import  re

start = 0
end = 0
tbContent={"name":"", "column":[]}

def reset():
	global start;
	global tbContent
	start = 0
	end =0
	for i in tbContent["column"]:
		print i,
	print "->",
	print tbContent["name"]
	#print "reset end"
	tbContent["name"] ="";
	tbContent["column"] = []

def process (line):

	global start
	global tbContent;
	#print "start =", start 

	if cmp(line[0:2], "--") == 0  or len(line) < 1:
		return 0;
	if cmp(line[0:6].upper(), "CREATE") == 0:
		#print "create start"
		start = 1
		spline = line.split()
		tbContent["name"] = spline[2]
		return
	#print line
	

	spline = line.split()
	if len(spline) < 1:
		return
	#if ((spline[0].find(')') > 0 and len(spline[0]) > 0 ) or (len(spline[0]) == 0 and spline[0] ==')' )):
	if line.find("=") > 0:
		#print "spline[0] =",  spline[0]
		reset();
		return 
	if start > 0 :		
		#print "spline=", spline[0]
		if spline[0].upper().replace(' ', '') in ("PRIMARY", "UNIQUE", "KEY" ):
			return 
		tbContent["column"].append(spline[0])
		return;


filename = "schema.sql"
filesql = open(filename)
try:
	#all_text = filesql.read()	
	for line in filesql.readlines():
		process (line)


finally:
	filesql.close()

	
	
print "end"
