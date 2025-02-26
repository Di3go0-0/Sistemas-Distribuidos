import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Configurar cliente
serverIP = "192.168.60.105"
serverPort = 1234
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

# Recibir clave pública del servidor
public_key = clientSocket.recv(4096)
rsa_public_key = RSA.import_key(public_key)

def recibir_mensajes():
    while True:
        try:
            # Recibir mensaje cifrado del servidor
            data = clientSocket.recv(4096)
            if not data:
                break
            
            # Descifrar con la clave pública del servidor
            cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
            decrypted_message = cipher_rsa.decrypt(base64.b64decode(data)).decode()
            print(f"\n[Cliente] Mensaje recibido: {decrypted_message}")
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break

# Iniciar un hilo para recibir mensajes
threading.Thread(target=recibir_mensajes, daemon=True).start()

def enviar_mensaje():
    while True:
        try:
            mensaje = input()
            
            # Cifrar mensaje antes de enviarlo
            cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
            encrypted_message = base64.b64encode(cipher_rsa.encrypt(mensaje.encode()))
            
            # Enviar mensaje cifrado al servidor
            clientSocket.sendall(encrypted_message)
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            break

# Iniciar un hilo para enviar mensajes
threading.Thread(target=enviar_mensaje, daemon=True).start()

while True:
    pass
