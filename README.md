# MQTT-Postgres-logger

Python3 service that subscribes to a wildcard feed of MQTT topics and stores them in a postgresql database. Topics are stored in a separate table.

INSTALLATION:
- copy config-default.py to config.py
- edit the values in config.py to match your setup
- create a database and a user for the logger
- run initialisedb.py to set up the tables
- create a user called `logging` in the group `other` and modify `mqtt-postgres.xml` as appropriate
- run `svccfg import mqtt-postgres.xml`

NOTE
- for a system that does not use svccfg, simply run `loggingserver.py` as a regular user and background it or install it as a service.
