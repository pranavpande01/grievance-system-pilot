import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Backend is running... waiting for messages")

while True:
    messages = r.xread({"chat_stream": "$"}, block=0, count=1)
    #print(messages)
    for i in r.xread({"chat_stream": "$"}, block=0, count=1):
        print(i)
    for events in messages:
        for msg_id, msg_data in events:
            print("User said:", msg_data["user_input"])
[
    [
        'chat_stream', 
        [('1757269370370-0', {'user': 'Jes'})]
    ]
]