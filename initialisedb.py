#!/usr/bin/env python3

import config
import psycopg2

try:
	conn = psycopg2.connect(
		"dbname='%s' user='%s' host='%s' password='%s'"%(
			config.DB,
			config.USER,
			config.PG_SERVER,
			config.PASS))
except:
	print("Error connecting to database")

cur = conn.cursor()

try:
	cur.execute("DROP TABLE IF EXISTS %s"%config.TABLE_DATA)
except:
	print("Cannot drop table '%s'"%config.TABLE_DATA)

try:
	cur.execute("DROP TABLE IF EXISTS %s"%config.TABLE_TOPICS)
except:
	print("Cannot drop table '%s'"%config.TABLE_TOPICS)
