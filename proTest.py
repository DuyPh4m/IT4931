from confluent_kafka import Producer

# Kafka broker configuration
brokers = ["kafka1:9093", "kafka2:9095", "kafka3:9097"]

# Kafka topic
topic = "test"

# Create Producer instance
producer_conf = {"bootstrap.servers": ",".join(brokers)}
producer = Producer(producer_conf)

# Produce a message to the topic
while True:
    message = "Hello, Kafka!"
    producer.produce(topic, value=message)

# Wait for any outstanding messages to be delivered and delivery reports received
    producer.flush()
