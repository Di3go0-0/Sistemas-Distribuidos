import os
import ssl
import socket
import threading

# Configuración del cliente
HOST = 'localhost'  # Se corrige el error de 'local_host'
PORT = 12345

# Verificar que los certificados existan
if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
    print("No se encontraron los certificados SSL. Ejecuta primero el servidor_chat_ssl.py")
    exit()

contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
contexto.load_verify_locations("cert.pem")

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_ssl = contexto.wrap_socket(cliente_socket, server_hostname="localhost")
cliente_ssl.connect((HOST, PORT))

print(f"Conectado al servidor SSL en {HOST}:{PORT}")

nombre_usuario = input("Ingresa tu nombre de usuario: ")
cliente_ssl.send(nombre_usuario.encode())

def recibir_mensajes():
    """ Hilo para recibir mensajes del servidor """
    while True:
        try:
            mensaje = cliente_ssl.recv(1024).decode()
            if not mensaje:
                break
            print(f"{mensaje}")
        except:
            break

# Iniciar hilo para recibir mensajes
threading.Thread(target=recibir_mensajes, daemon=True).start()

try:
    while True:
        mensaje = input()
        cliente_ssl.send(mensaje.encode())

except KeyboardInterrupt:
    print("\nDesconectando...")

finally:
    cliente_ssl.close()
    print("Cliente desconectado.")
