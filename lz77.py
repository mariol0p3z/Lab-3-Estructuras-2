class LZ77:
    def __init__(self, tamanio_ventana_busqueda, tamanio_ventana_prevista):
        self.tamanio_ventana_busqueda = tamanio_ventana_busqueda
        self.tamanio_ventana_prevista = tamanio_ventana_prevista

    def encontrarMatchLargo(self, datos, posicion_actual):
        fin_buffer = min(posicion_actual + self.tamanio_ventana_prevista, len(datos) + 1)

        mejor_match_distancia = -1
        mejor_match_longitud = -1

        for j in range(posicion_actual + 2, fin_buffer):
            indice_inicial = max(0, posicion_actual - self.tamanio_ventana_busqueda)
            substring = datos[posicion_actual:j]

            for i in range(indice_inicial, posicion_actual):
                repeticiones = len(substring) // (posicion_actual - i)

                ultimo = len(substring) % (posicion_actual - i)

                matched_string = datos[i:posicion_actual]*repeticiones + datos[i:i+ultimo]

                if matched_string == substring and len(substring) > mejor_match_longitud:
                    mejor_match_distancia = posicion_actual - i
                    mejor_match_longitud = len(substring)

        if mejor_match_distancia > 0 and mejor_match_longitud > 0:
            return (mejor_match_distancia, mejor_match_longitud)
        return None

    def comprimir(self, datos):
        i = 0
        datos_comprimidos = []

        while i<len(datos):
            match = self.encontrarMatchLargo(datos, i)

            if match:
                (best_offset, best_length) = match
                siguiente_caracter = datos[i+best_length] if i + best_length < len(datos) else ''
                datos_comprimidos.append((best_offset, best_length, siguiente_caracter))
                i += best_length + 1
            else:
                datos_comprimidos.append((0,0, datos[i]))
                i += 1

        return datos_comprimidos

    def descomprimir(self, datos_comprimidos):
        datos_descomprimidos = []

        for offset, length, siguiente_caracter in datos_comprimidos:
            if offset == 0 and length == 0:
                datos_descomprimidos.append(siguiente_caracter)
            else:
                inicio = len(datos_descomprimidos) - offset
                for i in range(length):
                    datos_descomprimidos.append(datos_descomprimidos[inicio + i])
                datos_descomprimidos.append(siguiente_caracter)

        return ''.join(datos_descomprimidos)