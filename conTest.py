from confluent_kafka import Consumer, KafkaError

# Kafka broker configuration
brokers = ["kafka1:9093", "kafka2:9095", "kafka3:9097"]

# Kafka topic
topic = "test"

# Create Consumer instance
consumer_conf = {
    "bootstrap.servers": ",".join(brokers),
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(consumer_conf)

# Subscribe to the topic
consumer.subscribe([topic])

# Poll for messages
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            continue
        else:
            print(msg.error())
            break

    # Process the received message
    print(f"Received message: {msg.value().decode('utf-8')}")

# Close the consumer
consumer.close()
