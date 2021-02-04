#!/usr/bin/python

import os
import sys
import json
import sqlite3
from datetime import date

from PyDictionary import PyDictionary

dictionary = PyDictionary

# looks up word
def look_up(w):
	return dictionary.meaning(w,disable_errors=True)
		
# prints formatted definition
def print_def(w,defs):
	print(word)
	for d in defs :
		print(d[0]+ ":")
		for sd in d[1]:
			print("\t",sd, "\n")
	
# START	
if len(sys.argv) > 1 :
	# get input from commandline
	word = sys.argv[1]

	# lookup word
	definition = look_up(word)

	# save current search to db
	if definition != None:
		conn = sqlite3.connect('VOCAB.db')
		cursor = conn.cursor()
		now = date.today()
		
		cursor.execute("CREATE TABLE IF NOT EXISTS VOCAB (WORD TEXT primary key, DEF TEXT, DATEADDED DATE)")
		defs = [(k,v) for k,v in definition.items()]
		
		try:	
			# some work on the defintion string to remove quotations that affect insert SQL statement
			defstr = ""
			for d in defs:
				defstr += str(d[0]) + ", " + str(d[1])
			defstr = defstr.replace('"', "'")

			# store definition in db, execute and commit query
			conn.execute("INSERT INTO VOCAB (WORD,DEF,DATEADDED) VALUES (?,?,?)", (json.dumps(word) , json.dumps(defstr),now))
			conn.commit()
			
			# print searched word
			print_def(word,defs)
		except sqlite3.IntegrityError:
			print("This word is in the db: ")
			print_def(word,defs)
		# close connection
		conn.close()
		print(word)
	else:
		print(word+ " - NOT FOUND")
		print("nothing added to db")
else:
	# no args - display all entries of previously searched words
	conn = sqlite3.connect('VOCAB.db')
	cursor = conn.cursor()
		
	cursor.execute("SELECT * FROM VOCAB")
	rows = cursor.fetchall()

	for r in rows:
		print("{}\n{}\n".format(r[0],r[1]))


		


