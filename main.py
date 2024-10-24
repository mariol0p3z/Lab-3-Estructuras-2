from arbolb import Arbol_B
import json
import os
from lz77 import LZ77
class main():
    def __init__(self):
        self.arbol = Arbol_B(3)
        self.carpeta_cartas = 'Cartas'
        self.lz77 = LZ77(20,10)
    
    def leerArchivo(self, nombre_archivo):
        with open(nombre_archivo, mode ='r', encoding='utf-8') as archivo:
            try:
                for linea in archivo:
                    separacion = linea.split(";")
                    
                    accion =  separacion[0]
                    dato_json = separacion[1].strip()

                    if dato_json.startswith('"') and dato_json.endswith('"'):
                        dato_json = dato_json[1:-1]
                        dato_json = dato_json.replace('""', '"')
                    
                    try:
                        dato = json.loads(dato_json)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar JSON: {e}")
                        continue
        
                    if accion == "INSERT":
                        self.arbol.insertar(dato)
                    elif accion == "PATCH":
                        self.arbol.actualizar(dato.get("dpi"), dato.get("name"), dato)
                    elif accion == "DELETE":
                        self.arbol.eliminar({"name": dato.get("name"), "dpi": dato.get("dpi")})
            except FileNotFoundError:
                print("Archivo no encontrado")
            finally:
                archivo.close()

    def leerCarta(self):
        nombre = input("Ingresa el nombre de la persona: ")
        dpi = input("Ingresa el DPI de la persona: ")

        archivo_cartas = [archivo for archivo in os.listdir(self.carpeta_cartas) if archivo.startswith(f"REC-{dpi}")]

        if not archivo_cartas:
            print(f"No se encontraron cartas con los datos ingresados...")
            return

        persona = self.arbol.buscar_por_nombre_y_dpi(dpi, nombre)

        if not persona:
            print(f"No se encontro a la persona dentro de la informacion guardada") 
            return

        for archivo_carta in archivo_cartas:
            ruta_archivo = os.path.join(self.carpeta_cartas, archivo_carta)
            try:
                with open(ruta_archivo, 'r', encoding = 'utf-8') as archivo:
                    contenido = archivo.read()
                
                datos_comprimidos = self.lz77.comprimir(contenido)

                numero_carta = archivo_carta.split('-')[-1].replace('.txt','')

                archivo_comprimido = os.path.join('Comprimidos', archivo_carta.replace('.txt', '_comprimido.txt'))

                with open(archivo_comprimido, 'w', encoding = 'utf-8') as salida:
                    for item in datos_comprimidos:
                        salida.write(f"{item}")
                print(f"Carta {numero_carta} procesada y comprimida")

                datos_descomprimidos = self.lz77.descomprimir(datos_comprimidos)

                archivo_descomprimido = os.path.join('Descomprimidos', archivo_carta.replace('.txt','_descomprimido.txt'))

                with open(archivo_descomprimido, 'w', encoding='utf-8') as salida:
                    salida.write(datos_descomprimidos)

                print(f"Carta {numero_carta} descomprimida y guardada como {archivo_descomprimido}")
 
            except FileNotFoundError:
                print(f"El archivo {ruta_archivo} no fue encontrado")
        
if __name__ == '__main__':
    programa = main()
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    programa.leerArchivo(nombre_archivo)
    programa.leerCarta()

#liza - 1041443605068
#bernice - 1053059170235