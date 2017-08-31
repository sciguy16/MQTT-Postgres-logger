#!/usr/bin/env python3

import config
import psycopg2
import psycopg2.extras
import paho.mqtt.client as mqtt

DISCOVERED_TOPICS={} # cache of topic IDs to avoid unnecessary database lookups

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

def topic_id(topic):
	"""
	Given a topic name, this function will first check the name to id mapping cached in memory
	(the `DISCOVERED_TOPICS` variable). Failing this, we look it up in the database in case it
	has been seen before but not by this instance. If the topic is not in the database then it
	is added and we return the generated topic id.
	"""
	if topic in DISCOVERED_TOPICS:
		# We know the topic id of the topic, so don't bother looking it up
		return DISCOVERED_TOPICS[topic]
	cur.execute("SELECT id FROM " + config.TABLE_TOPICS + " WHERE name='"+topic+"';")
	if cur.rowcount == 1:
		# the topic is in the database, so we remember it for later and return it
		tid = cur.fetchone()[0]
		DISCOVERED_TOPICS[topic] = tid
		return tid
	else:
		# Unknown topic, so we insert it into the database and remember its id for later
		cur.execute("INSERT INTO " + config.TABLE_TOPICS + "(name) VALUES ('"+topic+"') RETURNING id")
		tid = cur.fetchone()[0]
		conn.commit()
		DISCOVERED_TOPICS[topic] = tid
		return tid
		

def on_message(client,userdata,message):
	"""
	When a message is received we look up the topic id and then insert it into the data table.
	"""
	tid = topic_id(message.topic)
	print("Topic: %i"%tid)
	cur.execute("INSERT INTO " + config.TABLE_DATA + "(topic,data) VALUES (%s,%s)",
		(tid,str(message.payload.decode("utf-8"))))
	conn.commit()


mqtt_client = mqtt.Client("Logger")
mqtt_client.connect(config.MQTT_SERVER)
mqtt_client.on_message=on_message
mqtt_client.subscribe('#')
mqtt_client.loop_forever()
