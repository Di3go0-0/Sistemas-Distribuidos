import ssl
import os
import socket
import threading
import subprocess

# Función para generar el certificado SSL
def generar_certificado_ssl(cert_file="cert.pem", key_file="key.pem"):
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("Certificado SSL ya existe.")
        return
    
    cmd = [
        "openssl", "req", "-newkey", "rsa:2048", "-x509",
        "-keyout", key_file, "-out", cert_file, "-days", "365",
        "-nodes", "-subj", "/C=US/ST=CA/L=San Francisco/O=MyOrg/OU=MyUnit/CN=localhost"
    ]
    
    subprocess.run(cmd, check=True)
    print("Certificado SSL generado correctamente.")

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 12345
clientes = {}  # {nombre: socket}

# Generar certificado SSL si no existe
generar_certificado_ssl()

# Configurar SSL
contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
contexto.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Permitir hasta 5 conexiones en cola
server_socket.settimeout(1.0)  # Evita que accept() bloquee indefinidamente
print(f"Servidor SSL escuchando en {HOST}:{PORT}")

def notificar_conexion(nombre, conectado=True):
    """ Notifica a los clientes cuando alguien entra o sale del chat """
    mensaje = f"{'Conectado' if conectado else 'Desconectado'}: {nombre}"
    for usuario, c in clientes.items():
        try:
            c.send(mensaje.encode())
        except:
            continue

def manejar_cliente(cliente_ssl, addr):
    """ Maneja la comunicación con cada cliente """
    try:
        while True:
            cliente_ssl.send("Ingresa tu nombre de usuario: ".encode())
            nombre = cliente_ssl.recv(1024).decode().strip()

            if nombre in clientes:
                cliente_ssl.send("El nombre de usuario ya está en uso.".encode())
            else:
                break # Nombre de usuario válido

        clientes[nombre] = cliente_ssl
        print(f"Conectado: {nombre} desde {addr}")

        # Notificar a los demás clientes
        notificar_conexion(nombre, conectado=True)

        # Enviar lista de usuarios conectados
        lista_usuarios = "Usuarios conectados: " + ", ".join(clientes.keys())
        cliente_ssl.send(lista_usuarios.encode())

        while True:
            mensaje = cliente_ssl.recv(1024).decode()
            if not mensaje:
                break

            if mensaje == "/usuarios":
                lista_usuarios = "Usuarios conectados: " + ", ".join(clientes.keys())
                cliente_ssl.send(lista_usuarios.encode())
            elif mensaje.startswith("@"):
                try:
                    destinatario, mensaje_privado = mensaje.split(" ", 1)
                    destinatario = destinatario[1:]  # Quitar "@"
                    if destinatario in clientes:
                        clientes[destinatario].send(f"[Privado de {nombre}]: {mensaje_privado}".encode())
                    else:
                        cliente_ssl.send(f"El usuario {destinatario} no está conectado.".encode())
                except:
                    cliente_ssl.send("Formato incorrecto. Uso: @usuario mensaje".encode())
            else:
                for usuario, c in clientes.items():
                    if c != cliente_ssl:
                        c.send(f"[{nombre}]: {mensaje}".encode())

    except:
        print(f"Error con {nombre}.")

    finally:
        print(f"{nombre} se ha desconectado.")
        notificar_conexion(nombre, conectado=False)
        # Verificar que el usuario está en la lista antes de eliminarlo
        if nombre in clientes:
            del clientes[nombre]
        cliente_ssl.close()

# Manejo de conexiones
try:
    while True:
        try:
            cliente_socket, addr = server_socket.accept()
            cliente_ssl = contexto.wrap_socket(cliente_socket, server_side=True)
            threading.Thread(target=manejar_cliente, args=(cliente_ssl, addr), daemon=True).start()
        except socket.timeout:
            continue  # Permite que el servidor revise si se presionó CTRL + C

except KeyboardInterrupt:
    print("\nServidor cerrado por el usuario.")
finally:
    server_socket.close()
    print("Socket del servidor cerrado correctamente.")
