import pika
import json
from time import sleep
from mongoengine import connect, Document, StringField, BooleanField

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

connect('contacts_db')

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

def send_email_stub(contact_id):
    # Це ваша функція-заглушка для відправлення електронної пошти
    print(f"Sending email to contact with ID: {contact_id}")
    sleep(1)  # Імітуємо трошки затримку для емуляції надсилання пошти

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')

    if contact_id:
        contact = Contact.objects(id=contact_id, message_sent=False).first()

        if contact:
            send_email_stub(contact_id)
            contact.message_sent = True
            contact.save()

            print(f" [x] Email sent to {contact.full_name} - {contact.email}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='email_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()