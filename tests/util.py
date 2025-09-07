import redis
r = redis.Redis()

def send_user_message(thread_id, user_input):
    r.publish(f"incoming:{thread_id}", user_input)

def listen_for_response(thread_id):
    pubsub = r.pubsub()
    pubsub.subscribe(f"outgoing:{thread_id}")
    for message in pubsub.listen():
        if message['type'] == 'message':
            return message['data'].decode()
