import pika
import threading
import logging

logger = logging.getLogger(__name__)

class ThreadedConsumerPublisher(threading.Thread):

    def __init__(self, ampq_url):
        threading.Thread.__init__(self)
        parameters = pika.URLParameters(ampq_url)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self._stop_event = threading.Event()  # Thread stop signal
        self.lock = threading.Lock() # Lock for synchronizing

    def exchange_declare(self, exchange_name, exchange_type='topic'):
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    def queue_declare(self, queue_name):
        self.channel.queue_declare(queue=queue_name, auto_delete=False)

    def bind_queue(self, queue_name, exchange_name, routing_key):
        self.channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

    def consume_on_queue(self, queue_name, message_handler):
        self.channel.basic_consume(queue_name, on_message_callback=message_handler)

    def run(self):
        self.channel.start_consuming()

    def start_consumer(self):
        consumer_thread = threading.Thread(target=self.run)
        consumer_thread.start()

    def stop(self):
        logger.debug('Stopping consumer...')
        if self.channel.is_open:
            self.channel.stop_consuming()

        if self.connection.is_open:
            self.channel.close()
            self.connection.close()

        self._stop_event.set()  # Parar hilo

    def publish_message(self, exchange_name, routing_key, message):
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message
        )
        logger.info("Mensaje publicado: \"%s\" En el exchange: \"%s\" Mediante la routing key: \"%s\"",
                    message, exchange_name, routing_key)