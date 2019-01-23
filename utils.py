import random
import logging
import os
from gettext import gettext as _
log = logging.getLogger('utils')

def palabra_aleatoria(path, nivel):
    """retorna una palabra obtenida del archivo lista_palabras.txt"""
    path = path + 'nivel%s.palabra' %(nivel)
    archivo = open(path,'r')
    palabras = [palabra.lower() for palabra in archivo.readlines()]
    palabras.pop(0)
    archivo.close()   
    palabra_random = palabras[random.randint(0, len(palabras)-1)]    
    log.debug(palabra_random)
    palabra_random = palabra_random.replace('"','')
    return palabra_random.split(':')

def validar_uri(uri):
    log.debug('validar uri')
    lista = uri.split('.')
    if 'palabra' in lista[1]:
        return 1
    else:
        return 0

def categoria_personalizada(path):
    if os.path.exists(path + 'nivel8.palabra'):
        return 8
    else:
        return 0

def importar_lista_p(path ,uri, nivel):
    '''importa una nueva lista de palabras'''
    if validar_uri(uri):
        log.debug('palabra importada')
        path = path + 'nivel%s.palabra' %(nivel + 1)
        archivo = open(uri, 'r') #lee el archivo a exportar
        if (nivel + 1) is 8:
            archivo_viejo = open(path, 'w')
        else:
            archivo_viejo = open(path, 'r+w')
        archivo_viejo.seek(0, os.SEEK_END)
        texto = archivo.read()
        archivo_viejo.write(texto)
        archivo_viejo.close()
        archivo.close()

