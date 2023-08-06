import threading
import pika
import time

class RabbitSender:
    def __init__(self, host='localhost', port='5672', username=None, password=None, virtual_host='/'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.connection = None
        self.channel = None
        self.heartbeat_channel = None
        self.heartbeat_thread = None
        self.is_heartbeat_running = False
        self.lock = threading.Lock()

    def connect(self):
        # Set connection parameters
        credentials = pika.PlainCredentials(self.username, self.password) if self.username and self.password else None
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.virtual_host,
                                               credentials=credentials)

        # Establish connection to RabbitMQ server
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Start heartbeat thread
        self.heartbeat_channel = self.connection.channel()
        self.is_heartbeat_running = True
        self.heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        self.heartbeat_thread.start()

    def send_heartbeat(self):
        while self.is_heartbeat_running:
            try:
                self.lock.acquire()
                self.connection.process_data_events()
            except Exception as e:
                raise e
            finally:
                self.lock.release()
            time.sleep(5)

    def send_message(self, exchange, routing_key, msg_type, message, headers={}):
        try:
            properties = pika.BasicProperties(
                correlation_id=str(msg_type),
                headers=headers
            )
            self.lock.acquire()
            self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=properties)
        except pika.exceptions.AMQPConnectionError as e:
            raise ConnectionError('Error sending message to ATOM')

        except pika.exceptions.AMQPChannelError as e:
            raise ConnectionError('Error sending message to ATOM')
        finally:
            self.lock.release()

    def close(self):
        self._stop_heartbeat_thread()
        if self.connection:
            self.connection.close()

    def _stop_heartbeat_thread(self):
        self.is_heartbeat_running = False
        self.heartbeat_thread.join()
