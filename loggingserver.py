#!/usr/bin/env python3

import config
import psycopg2
import psycopg2.extras
import paho.mqtt.client as mqtt

DISCOVERED_TOPICS={}

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
	if topic in DISCOVERED_TOPICS:
		print("known topic")
		return DISCOVERED_TOPICS[topic]
	cur.execute("SELECT id FROM " + config.TABLE_TOPICS + " WHERE name='"+topic+"';")
	if cur.rowcount == 1:
		print("topic is in database")
		row = cur.fetchone()
		tid = row[0]
		print(tid)
		DISCOVERED_TOPICS[topic] = tid
		return tid
	else:
		print("adding topic to database")
		cur.execute("INSERT INTO " + config.TABLE_TOPICS + "(name) VALUES ('"+topic+"') RETURNING id")
		tid = cur.fetchone()[0]
		print(tid)
		conn.commit()
		return tid
		

def on_message(client,userdata,message):
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	print("message retain flag=",message.retain)
	tid = topic_id(message.topic)
	print("Topic: %i"%tid)


mqtt_client = mqtt.Client("Logger")
mqtt_client.connect(config.MQTT_SERVER)
mqtt_client.on_message=on_message
mqtt_client.subscribe('#')
mqtt_client.loop_forever()
