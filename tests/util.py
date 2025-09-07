import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Backend is running... waiting for messages")

while True:
    messages = r.xread({"chat_stream": "$"}, block=0, count=1)
    #print(messages)
    for stream, events in messages:
        for msg_id, msg_data in events:
            print("User said:", msg_data["user_input"])
