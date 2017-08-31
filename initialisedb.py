#!/usr/bin/env python3

import config
import psycopg2
import psycopg2.extras

try:
	conn = psycopg2.connect(
		"dbname='%s' user='%s' host='%s' password='%s'"%(
			config.DB,
			config.USER,
			config.PG_SERVER,
			config.PASS))
except:
	print("Error connecting to database")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

print("Dropping old tables...")
try:
	cur.execute("DROP TABLE IF EXISTS %s"%config.TABLE_DATA)
except:
	print("Cannot drop table '%s'"%config.TABLE_DATA)

try:
	cur.execute("DROP TABLE IF EXISTS %s"%config.TABLE_TOPICS)
except:
	print("Cannot drop table '%s'"%config.TABLE_TOPICS)

print("Creating fresh tables...")

try:
	cur.execute("""
		CREATE TABLE """ + config.TABLE_DATA + """ (
			id SERIAL PRIMARY KEY,
			topic INTEGER NOT NULL,
			data jsonb,
			time timestamptz NOT NULL DEFAULT now()
		);""")
except:
	print("Error creating table " + config.TABLE_DATA)

try:
	cur.execute("""
		CREATE TABLE """ + config.TABLE_TOPICS + """ (
			id SERIAL PRIMARY KEY,
			name VARCHAR(255) NOT NULL
		);""")
except:
	print("Error creating table " + config.TABLE_TOPICS)

conn.commit()
conn.close()
print("Success!")
