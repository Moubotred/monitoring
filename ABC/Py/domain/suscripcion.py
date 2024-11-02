import json

class ComandoSuscripcion:
    # Ruta al archivo JSON
    ruta_archivo = 'Users.json'

    def ejecutar(self,id,verifi):
        if self.consultar_usuario(id) == True:
            comand()

    def agregar_usuario(self,id,verifi):
        datos = {
            f"{id}": {verifi},
        }
        # Escribir el diccionario en el archivo JSON
        with open(self.ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

    def consultar_usuario(self,id):
        with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos[id]
            

