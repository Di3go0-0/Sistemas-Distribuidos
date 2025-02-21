import socket
import threading

# Crear un socket para el cliente
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Dirección IP y puerto del servidor
serverIP = "192.168.60.105"
serverPort = 1234

# Conectar al servidor
clientSocket.connect((serverIP, serverPort))

# Función para recibir mensajes de otros clientes
def recibir_mensajes():
    while True:
        try:
            # Intentar recibir mensajes del servidor
            data = clientSocket.recv(1024)
            if not data:
                break  # Si no hay datos, cerrar conexión
            print(f"\nMensaje recibido: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break

# Iniciar un hilo para recibir mensajes
threading.Thread(target=recibir_mensajes, daemon=True).start()

# Función para enviar mensajes
def enviar_mensaje():
    while True:
        try:
            mensaje = input()  # Capturar mensaje del usuario
            clientSocket.sendall(mensaje.encode('utf-8'))  # Enviar al servidor
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            break

# Iniciar un hilo para enviar mensajes
threading.Thread(target=enviar_mensaje, daemon=True).start()

# Mantener el programa corriendo para recibir y enviar mensajes
while True:
    pass