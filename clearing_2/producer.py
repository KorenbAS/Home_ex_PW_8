import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField

fake = Faker()
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

connect('contacts_db')

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

def send_fake_contacts(num_contacts):
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()

        contact = Contact(full_name=full_name, email=email)
        contact.save()

        message = {'contact_id': str(contact.id)}
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=json.dumps(message))

        print(f" [x] Sent {full_name} - {email}")

    connection.close()

send_fake_contacts(5)