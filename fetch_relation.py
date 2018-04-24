#-*-coding:utf-8-*-


import  re

start = 0
end = 0
tbContent={"name":"", "column":[]}

filew = open("output.txt", "w")
file_overview = open("output_overview.txt", "w")
header = '''
digraph g{
size = "900, 400";

node [shape=box, style=filled, fillcolor=orange, fontsize=10];
#graph [rankdir=lr]
arrowsize = 10

edge[weight = 10, style=dotted]
'''
filew.write(header)

def reset():
	global start;
	global tbContent
	global filew;
	start = 0
	end =0
	for i in tbContent["column"]:
		print i,
	print "->",
	print tbContent["name"]
	for i in tbContent["column"]:
		#filew.write(i+"-> " + tbContent["name"]+";\n")
		filew.write( tbContent["name"]+"-> " +i +";\n")
		#filew.write("-> ")
		#filew.write(tbContent["name"]+"\n")


	for i in tbContent["column"]:
		file_overview.write(i + " ")
	file_overview.write(tbContent["name"].upper()+";\n")
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

filew.write("\n}");
filew.close()
file_overview.close()

print "end"
