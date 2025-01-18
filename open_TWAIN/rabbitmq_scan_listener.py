import pika
import subprocess

# Config
RABBITMQ_HOST = 'localhost'  # Change
QUEUE_NAME = 'scan_start_queue'  # Change

def on_message(ch, method, properties, body):

    print(f"Mensagem recebida: {body.decode('utf-8')}")

    try:
        # Execute scan_start.py
        print("Iniciando o script de digitalização...")
        subprocess.run(['python', 'scan_start.py'], check=True)
        print("Script de digitalização concluído.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script scan_start: {e}")

# Conecting to RabbitMQ
print("Conectando ao RabbitMQ...")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)
print(f"Fila '{QUEUE_NAME}' pronta para receber mensagens.")

# Listening for messages
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=True)
print("Aguardando mensagens. Pressione CTRL+C para sair.")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Interrompido pelo usuário.")
finally:
    connection.close()
    print("Conexão com o RabbitMQ encerrada.")
