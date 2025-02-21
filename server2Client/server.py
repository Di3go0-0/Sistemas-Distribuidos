import socket
import threading

def handle_client_to_client(client1_socket, client2_socket):
    """Maneja la comunicación entre dos clientes."""
    try:
        while True:
            # Recibir datos de cliente 1
            data_from_client1 = client1_socket.recv(1024)
            if not data_from_client1:
                break  # Si no hay más datos, se cierra la conexión

            print(f"Recibido de Cliente 1: {data_from_client1.decode()}")
            # Reenviar los datos de Cliente 1 a Cliente 2
            client2_socket.send(data_from_client1)

            # Recibir datos de cliente 2
            data_from_client2 = client2_socket.recv(1024)
            if not data_from_client2:
                break  # Si no hay más datos, se cierra la conexión

            print(f"Recibido de Cliente 2: {data_from_client2.decode()}")
            # Reenviar los datos de Cliente 2 a Cliente 1
            client1_socket.send(data_from_client2)

    except Exception as e:
        print(f"Error durante la comunicación: {e}")
    finally:
        client1_socket.close()
        client2_socket.close()

def start_bridge_server():
    """Inicia el servidor que actúa como puente entre dos clientes."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configurar el servidor
    server_socket.bind(("192.168.60.105", 1234))  # Usa la IP y el puerto que necesites
    server_socket.listen(2)  # Escucha dos conexiones (para los dos clientes)

    print("Esperando a que se conecten los clientes...")

    # Aceptar conexiones de los dos clientes
    client1_socket, client1_address = server_socket.accept()
    print(f"Cliente 1 conectado desde {client1_address}")

    client2_socket, client2_address = server_socket.accept()
    print(f"Cliente 2 conectado desde {client2_address}")

    # Crear un hilo para manejar la comunicación entre los dos clientes
    client_thread = threading.Thread(target=handle_client_to_client, args=(client1_socket, client2_socket))
    client_thread.start()
    
    server_socket.close()

if __name__ == "__main__":
    start_bridge_server()