import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Generar claves RSA
key = RSA.generate(2048)
public_key = key.publickey().export_key()
private_key = key.export_key()

def handle_client(client_socket, client_id, other_client_socket):
    """Maneja la comunicación con los clientes usando RSA."""
    try:
        # Enviar clave pública al cliente
        client_socket.send(public_key)

        while True:
            # Recibir datos del cliente
            data = client_socket.recv(4096)
            if not data:
                break

            # Descifrar mensaje con clave privada
            cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
            decrypted_message = cipher_rsa.decrypt(base64.b64decode(data)).decode()
            print(f"[Servidor] Cliente {client_id} envió: {decrypted_message}")

            # Cifrar el mensaje de nuevo para el otro cliente
            cipher_rsa_other = PKCS1_OAEP.new(RSA.import_key(public_key))
            encrypted_for_other = base64.b64encode(cipher_rsa_other.encrypt(decrypted_message.encode()))

            # Enviar mensaje cifrado al otro cliente
            other_client_socket.send(encrypted_for_other)

    except Exception as e:
        print(f"Error con Cliente {client_id}: {e}")
    finally:
        client_socket.close()

def start_bridge_server():
    """Inicia el servidor."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.60.105", 1234))
    server_socket.listen(2)

    print("Esperando a que se conecten los clientes...")

    client1_socket, client1_address = server_socket.accept()
    print(f"Cliente 1 conectado desde {client1_address}")

    client2_socket, client2_address = server_socket.accept()
    print(f"Cliente 2 conectado desde {client2_address}")

    # Iniciar hilos para manejar la comunicación con cada cliente
    client1_thread = threading.Thread(target=handle_client, args=(client1_socket, 1, client2_socket))
    client2_thread = threading.Thread(target=handle_client, args=(client2_socket, 2, client1_socket))

    client1_thread.start()
    client2_thread.start()

    client1_thread.join()
    client2_thread.join()

    server_socket.close()

if __name__ == "__main__":
    start_bridge_server()
