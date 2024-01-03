from confluent_kafka import Producer
from datetime import datetime
import time
import csv

# brokers = ["kafka1:9093", "kafka2:9095", "kafka3:9097"]

brokers = ["kafka1:9092", "kafka2:9092"]

producer_conf = {"bootstrap.servers": ",".join(brokers)}
producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
  
def send_message(producer, topic, csv_path):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        current_timestamp = None

        for row in csv_reader:
            # Extract DateTime from the row
            date_time_str = row['DateTime']
            date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')
            timestamp = date_time.strftime('%Y-%m-%d')
            # Check if it's a new group

            if current_timestamp != timestamp:
                # Pause for 5 seconds before sending a record in a new group
                time.sleep(1)
                current_timestamp = timestamp
            # Send the record to Kafka
            producer.produce(topic, key=str(timestamp), value=str(row), callback=delivery_report)
            producer.flush()

if __name__ == '__main__':
    try:
        send_message(producer, 'epl', './data/results.csv')
    except Exception as e:
        print(e)