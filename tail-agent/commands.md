# Commands to start or stop the tail process

curl -X POST http://127.0.0.1:5000/start -H "Content-Type: application/json" -d '{"filepath": "new.txt"}'
culr -X GET http://127.0.0.1:5000/stop
