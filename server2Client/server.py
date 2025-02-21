import socket
import threading

def handle_client(client_socket, client_id, other_client_socket):
    """Maneja la comunicación de un cliente con el otro cliente."""
    try:
        while True:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if not data:
                break  # Si no hay datos, el cliente se desconecta

            print(f"Recibido de Cliente {client_id}: {data.decode()}")
            # Enviar el mensaje al otro cliente
            other_client_socket.send(data)

    except Exception as e:
        print(f"Error con Cliente {client_id}: {e}")
    finally:
        client_socket.close()

def start_bridge_server():
    """Inicia el servidor que actúa como puente entre dos clientes."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configuración del servidor
    server_socket.bind(("192.168.60.105", 1234))  # Usa la IP y el puerto que necesites
    server_socket.listen(2)  # Escucha dos conexiones (para los dos clientes)

    print("Esperando a que se conecten los clientes...")

    # Aceptar conexiones de los dos clientes
    client1_socket, client1_address = server_socket.accept()
    print(f"Cliente 1 conectado desde {client1_address}")

    client2_socket, client2_address = server_socket.accept()
    print(f"Cliente 2 conectado desde {client2_address}")

    # Iniciar hilos para manejar la comunicación con cada cliente
    client1_thread = threading.Thread(target=handle_client, args=(client1_socket, 1, client2_socket))
    client2_thread = threading.Thread(target=handle_client, args=(client2_socket, 2, client1_socket))

    client1_thread.start()
    client2_thread.start()

    # Esperar a que ambos hilos terminen
    client1_thread.join()
    client2_thread.join()

    server_socket.close()

if __name__ == "__main__":
    start_bridge_server()
