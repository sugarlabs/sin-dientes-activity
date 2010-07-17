#Ahorcado
import gtk
import logging
from gettext import gettext as _
from sugar.activity import activity

import utils

_logger = logging.getLogger('ahorcado-activity')
_logger.setLevel(logging.DEBUG)

class Ahorcado:

    def __init__(self):

        #ventana
        self.ventana = gtk.Window()
        self.ventana.set_title(_('Ahorcado'))
        self.ventana.connect('key-press-event', self._key_press_cb)
        self.ventana.connect('destroy', self._destroy_cb)
        
        #contenedores
        self.contenedor = gtk.VBox()
        self.ventana.add(self.contenedor)

        self.contenedor_superior = gtk.HBox()
        self.contenedor_inferior= gtk.HBox()
        
        self.contenedor.pack_start(self.contenedor_superior)
        self.contenedor.pack_start(self.contenedor_inferior, expand=False)

        self.subcontenedor= gtk.VBox()
                
        #interface
        self.imagen = gtk.Image()
        self.instrucciones_label = gtk.Label('Instrucciones')
        self.aciertos_label = gtk.Label('Puntaje: 0')
        self.errores_label = gtk.Label('Errores: 0')
        self.palabra_label = gtk.Label()
        self.letrasusadas_label = gtk.Label('Letras Usadas: ')
        self.palabra_entry = gtk.Entry()
        self.ok_btn = gtk.Button(_('Ok'))
        self.ok_btn.connect('clicked', self._ok_btn_clicked_cb, None)
        self.nuevojuego_btn = gtk.Button(_('Nuevo Juego'))
        self.nuevojuego_btn.connect('clicked', self._nuevojuego_btn_clicked_cb, None)
        self._cambiar_imagen(0)

        self.creacion() # Crea las variables necesarias para el comienzo del juego

        #agregando elementos
        self.contenedor_superior.pack_start(self.imagen)
        self.contenedor_superior.pack_start(self.subcontenedor)
        self.subcontenedor.pack_start(self.instrucciones_label)
        self.subcontenedor.pack_start(self.aciertos_label)
        self.subcontenedor.pack_start(self.letrasusadas_label)
        self.subcontenedor.pack_start(self.errores_label)
        self.subcontenedor.pack_start(self.palabra_label)
        self.subcontenedor.pack_start(self.nuevojuego_btn)

        self.contenedor_inferior.pack_start(self.palabra_entry)
        self.contenedor_inferior.pack_start(self.ok_btn, False)
        
        self.contenedor.show_all()
        self.nuevojuego_btn.hide()
        self.ventana.show()

    def creacion(self):
        '''Crea las variables necesarias para el comienzo del juego'''
        self.aciertos = 0 #Cuenta los aciertos de letras en la palabra secreta
        self.errores = 0 #Cuenta los errores de letras en la palabra secreta
        self.l_aciertos = [] #Lista de letras acertadas en la palabra secreta
        self.l_errores = [] #Lista de letras erradas en la palabra secreta
        self.palabra = utils.palabra_aleatoria() #Crea una palabra aleatoria

    def _ok_btn_clicked_cb(self, widget, data=None):
        self._actualizar_palabra()

    def _nuevojuego_btn_clicked_cb(self, widget, data=None):
        self.creacion()
        self.aciertos_label.set_text('Puntaje: 0')
        self.errores_label.set_text('Errores: 0')
        self.letrasusadas_label.set_text('Letras Usadas: ')
        self.instrucciones_label.set_text('Instrucciones')
        self.palabra_label.set_text("")
        self.nuevojuego_btn.hide()
        self._cambiar_imagen(0)

    def _cambiar_imagen(self, level):
        _logger.debug('level: %s' % level)
        ruta = 'resources/%s.jpg' % level
        self.imagen.set_from_file(ruta)

    def _key_press_cb(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        _logger.debug('keyname: %s' % keyname)
        if keyname == 'Return':
            self._actualizar_palabra()
        return False

    def read_file(self, filepath):
        pass

    def write_file(self, filepath):
        pass

    def main(self):
        gtk.main()

    def _destroy_cb(self, widget, data=None):
        gtk.main_quit()

    def _actualizar_palabra(self):

        #Convierte la letra a minuscula
        letra_actual = self.palabra_entry.get_text().lower()
        _logger.debug('letra_actual: %s' % letra_actual)

        #Evalua si se escribio mas de 1 letra o esta vacio
        if (len(letra_actual) is not 1 or letra_actual == " "): 
            self.palabra_entry.set_text('')
            _logger.debug('mas de una letra o vacio')
            self.instrucciones_label.set_text(_("Instruciones:\nIntroduzca solo una letra!"))
        
        #Evalua si letra esta dentro de palabra
        elif (letra_actual in self.palabra and letra_actual not in self.l_aciertos):
            self.l_aciertos.append(letra_actual)
            
            for i in range(len(self.palabra)):
                if (letra_actual == self.palabra[i]):
                    self.aciertos += 1
            
            self.palabra_entry.set_text('')
            _logger.debug('letra dentro de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self.instrucciones_label.set_text(_("Instruciones:\nLetra dentro de palabra secreta!"))
            self.aciertos_label.set_text(_('Puntaje: %s' % self.aciertos))
            self.letrasusadas_label.set_text(_('Letras Usadas: %s' % self.l_aciertos))
            self.errores_label.set_text(_('Errores: %s' % self.errores))
            
            #Evalua si se acerto la palabra y temina el juego
            if (self.aciertos == len(self.palabra)): 
                _logger.debug('acerto palabra')
                self.instrucciones_label.set_text(_('Instruciones:\nAcertastes la palabra secreta, FELICIDADES! x)'))

        #Evalua si letra es repetida y esta dentro de palabra
        elif (letra_actual in self.palabra and letra_actual in self.l_aciertos): 
            self.palabra_entry.set_text('')
            _logger.debug('letra repetida y dentro de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self.instrucciones_label.set_text(_("Instruciones:\nLetra repedita y dentro de palabra secreta!"))
            self.aciertos_label.set_text(_('Puntaje: %s' % self.aciertos))
            self.letrasusadas_label.set_text(_('Letras Usadas: %s' % self.l_aciertos))
            self.errores_label.set_text(_('Errores: %s' % self.errores))

        #Evalua si letra no esta dentro de palabra
        elif (letra_actual not in self.palabra and letra_actual not in self.l_errores):
            self.l_errores.append(letra_actual)
            self.errores += 1
            self._cambiar_imagen(self.errores)
            self.palabra_entry.set_text('')
            _logger.debug('letra fuera de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self.instrucciones_label.set_text(_("Instruciones:\nLetra fuera de palabra secreta!"))
            self.aciertos_label.set_text(_('Puntaje: %s' % self.aciertos))
            self.letrasusadas_label.set_text(_('Letras Usadas: %s' % self.l_aciertos))
            self.errores_label.set_text(_('Errores: %s' % self.errores))
            
            #Evalua si se completo el ahorcado y temina el juego            
            if (self.errores >= 8): 
                _logger.debug('fin del juego')
                self.instrucciones_label.set_text(_('Instruciones:\nLa palabra secreta era %s, Fin del juego! x(' % self.palabra) )
                self.nuevojuego_btn.show() # muestra el boton para comenzar el juego
                pass

        #Evalua si letra es repetida y no dentro de palabra
        elif (letra_actual not in self.palabra and letra_actual in self.l_errores): 
            self.palabra_entry.set_text('')
            _logger.debug('letra repetida y fuera de palabra, aciertos: %s, errores: %s' %(self.aciertos, self.errores))
            self.instrucciones_label.set_text(_("Instruciones:\nLetra repetida y fuera de palabra secreta!"))
            self.aciertos_label.set_text(_('Puntaje: %s' % self.aciertos))
            self.letrasusadas_label.set_text(_('Letras Usadas: %s' % self.l_aciertos))
            self.errores_label.set_text(_('Errores: %s' % self.errores))
        pista = ''
        for letra in self.palabra:
            if letra in self.l_aciertos:
                pista += '%s ' % letra
            else:
                pista += '_ '
        self.palabra_label.set_text(pista)
        
if __name__ == "__main__":
    foo = Ahorcado()
    foo.main()
