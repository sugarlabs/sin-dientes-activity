# -*- coding: UTF-8 -*-

# Sin-dientes-activity
# Copyright (C) 2012, Yader Velásquez

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Yader Velásquez <yajosev@gmail.com>


from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from gi.repository import Gtk
from gi.repository import Gdk
import logging
from gettext import gettext as _
import os
import utils
from gi.repository import Pango

_logger = logging.getLogger('sindiente-activity')


class Sindiente(activity.Activity):

    def __init__(self, handle):
        super(Sindiente, self).__init__(handle)
        # ventana
        self.nivel = None
        self.set_title(_('Sin Dientes'))
        self.carpeta_imagen = 'resources/personaje_'
        self.sugar_data = self.get_activity_root() + '/data/'
        self.connect('key-press-event', self._key_press_cb)

        # Barra de herramientas sugar

        toolbar_box = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        # general
        self.comprobar_interfaz = False
        self.modificar_text = Pango.FontDescription("Bold 10")
        self._archivo_sugar()

        # contenedores
        self.contenedor = Gtk.VBox()
        self.contenedor_superior = Gtk.HBox()
        self.contenedor_inferior = Gtk.HBox()
        self.contenedor.pack_start(self.contenedor_superior, True, True, 0)
        self.contenedor.pack_start(self.contenedor_inferior, False, True, 0)
        self.subcontenedor = Gtk.VBox()
        self.contenedor_nivel = Gtk.VBox()
        self.contenedor_nivel_1 = Gtk.VBox()
        self.contenedor_nivel_2 = Gtk.VBox()
        self.contenedor_instruc = Gtk.VBox()
        self.contenedor_instruc_1 = Gtk.HBox()
        self.contenedor_instruc_2 = Gtk.HBox()
        self.contenedor_instruc_3 = Gtk.HBox()
        self.contenedor_instruc_4 = Gtk.HBox()
        self.contenedor_np_v = Gtk.VBox()
        self.contenedor_np_1 = Gtk.HBox()
        self.contenedor_np_2 = Gtk.HBox()

        # Elegir personaje
        self.elegir_personaje_v = Gtk.VBox()
        self.elegir_personaje_1 = Gtk.HBox()
        self.elegir_personaje_2 = Gtk.HBox()
        self.boton_personaje_1 = Gtk.HBox()
        self.boton_personaje_2 = Gtk.HBox()

        self.text_boton_nino = _('Elegir')
        self.btn_nino_1 = Gtk.Button(self.text_boton_nino)
        self.btn_nino_2 = Gtk.Button(self.text_boton_nino)
        self.btn_nino_3 = Gtk.Button(self.text_boton_nino)
        self.btn_nina_1 = Gtk.Button(self.text_boton_nino)
        self.btn_nina_2 = Gtk.Button(self.text_boton_nino)
        self.btn_nina_3 = Gtk.Button(self.text_boton_nino)
        self.btn_nino_1.connect('clicked', self._btn_nino_1_cb)
        self.btn_nino_2.connect('clicked', self._btn_nino_2_cb)
        self.btn_nino_3.connect('clicked', self._btn_nino_3_cb)
        self.btn_nina_1.connect('clicked', self._btn_nina_1_cb)
        self.btn_nina_2.connect('clicked', self._btn_nina_2_cb)
        self.btn_nina_3.connect('clicked', self._btn_nina_3_cb)

        # niños
        self.personaje_label = Gtk.Label(label=_("Elige un personaje"))
        self.personaje_label.modify_font(self.modificar_text)
        self.nino_1 = Gtk.Image()
        self.nino_1.set_from_file('resources/personaje_1/00.png')
        self.nino_2 = Gtk.Image()
        self.nino_2.set_from_file('resources/personaje_2/00.png')
        self.nino_3 = Gtk.Image()
        self.nino_3.set_from_file('resources/personaje_3/00.png')

        self.nina_1 = Gtk.Image()
        self.nina_1.set_from_file('resources/personaje_4/00.png')
        self.nina_2 = Gtk.Image()
        self.nina_2.set_from_file('resources/personaje_5/00.png')
        self.nina_3 = Gtk.Image()
        self.nina_3.set_from_file('resources/personaje_6/00.png')

        self.boton_personaje_1.pack_start(self.btn_nino_1, True, False, 0)
        self.boton_personaje_1.pack_start(self.btn_nino_2, True, False, 0)
        self.boton_personaje_1.pack_start(self.btn_nino_3, True, False, 0)
        self.boton_personaje_2.pack_start(self.btn_nina_1, True, False, 0)
        self.boton_personaje_2.pack_start(self.btn_nina_2, True, False, 0)
        self.boton_personaje_2.pack_start(self.btn_nina_3, True, False, 0)

        self.elegir_personaje_1.pack_start(self.nino_1, True, True, 0)
        self.elegir_personaje_1.pack_start(self.nino_2, True, True, 0)
        self.elegir_personaje_1.pack_start(self.nino_3, True, True, 0)
        self.elegir_personaje_2.pack_start(self.nina_1, True, True, 0)
        self.elegir_personaje_2.pack_start(self.nina_2, True, True, 0)
        self.elegir_personaje_2.pack_start(self.nina_3, True, True, 0)

        self.elegir_personaje_v.pack_start(self.personaje_label, True, True, 0)
        self.elegir_personaje_v.pack_start(
            self.elegir_personaje_1, True, True, 0)
        self.elegir_personaje_v.pack_start(
            self.boton_personaje_1, False, True, 0)
        self.elegir_personaje_v.pack_start(
            self.elegir_personaje_2, True, True, 0)
        self.elegir_personaje_v.pack_start(
            self.boton_personaje_2, False, True, 0)
        self.elegir_personaje_v.show_all()
        self.set_canvas(self.elegir_personaje_v)

        # importing categories

        categoria_nivel_1 = open(self.sugar_data + 'nivel1.palabra')
        palabras_nivel_1 = categoria_nivel_1.readlines()
        palabras_nivel_1 = map(lambda s: s.strip(), palabras_nivel_1)

        categoria_nivel_2 = open(self.sugar_data + 'nivel2.palabra')
        palabras_nivel_2 = categoria_nivel_2.readlines()
        palabras_nivel_2 = map(lambda s: s.strip(), palabras_nivel_2)

        categoria_nivel_3 = open(self.sugar_data + 'nivel3.palabra')
        palabras_nivel_3 = categoria_nivel_3.readlines()
        palabras_nivel_3 = map(lambda s: s.strip(), palabras_nivel_3)

        categoria_nivel_4 = open(self.sugar_data + 'nivel4.palabra')
        palabras_nivel_4 = categoria_nivel_4.readlines()
        palabras_nivel_4 = map(lambda s: s.strip(), palabras_nivel_4)

        categoria_nivel_5 = open(self.sugar_data + 'nivel5.palabra')
        palabras_nivel_5 = categoria_nivel_5.readlines()
        palabras_nivel_5 = map(lambda s: s.strip(), palabras_nivel_5)

        categoria_nivel_6 = open(self.sugar_data + 'nivel6.palabra')
        palabras_nivel_6 = categoria_nivel_6.readlines()
        palabras_nivel_6 = map(lambda s: s.strip(), palabras_nivel_6)

        categoria_nivel_7 = open(self.sugar_data + 'nivel7.palabra')
        palabras_nivel_7 = categoria_nivel_7.readlines()
        palabras_nivel_7 = map(lambda s: s.strip(), palabras_nivel_7)

        # interface menu
        self.imagen_menu = Gtk.Image()
        self.nivel_1 = Gtk.Button(palabras_nivel_1[0])
        self.nivel_1.connect('clicked', self._nivel_uno_cb, None)
        self.nivel_2 = Gtk.Button(palabras_nivel_2[0])
        self.nivel_2.connect('clicked', self._nivel_dos_cb, None)
        self.nivel_3 = Gtk.Button(palabras_nivel_3[0])
        self.nivel_3.connect('clicked', self._nivel_tres_cb, None)
        self.nivel_4 = Gtk.Button(palabras_nivel_4[0])
        self.nivel_4.connect('clicked', self._nivel_cuatro_cb, None)
        self.nivel_5 = Gtk.Button(palabras_nivel_5[0])
        self.nivel_5.connect('clicked', self._nivel_cinco_cb, None)
        self.nivel_6 = Gtk.Button(palabras_nivel_6[0])
        self.nivel_6.connect('clicked', self._nivel_seis_cb, None)
        self.nivel_7 = Gtk.Button(palabras_nivel_7[0])
        self.nivel_7.connect('clicked', self._nivel_siete_cb, None)
        self.importar_btn = Gtk.Button(_('Agregar lista de palabra'))
        self.importar_btn.connect('clicked', self._importar_cb, None)
        self.instrucciones = Gtk.Button(_('Instrucciones de juego'))
        self.instrucciones.connect('clicked', self._instrucciones_cb, None)
        self.nuevapalabra_btn = Gtk.Button(_('Modo Versus'))
        self.nuevapalabra_btn.connect('clicked', self._nuevapalabra_cb, None)
        self.cambiar_personaje_btn = Gtk.Button(_('Cambiar personaje'))
        self.cambiar_personaje_btn.connect(
            'clicked', self._cambiar_personaje_cb)
        self.categoria_libre = Gtk.Button(_('Categoría Personalizada'))
        self.categoria_libre.connect(
            'clicked', self._categoria_personalizada_cb)
        self.bienvenida = Gtk.Label(label=_('Bienvenido a \"Sin Diente\"'))
        self.bienvenida.modify_font(self.modificar_text)

        # agregando elementos de menú
        self.contenedor_nivel_h = Gtk.HBox()
        self.contenedor_nivel.pack_start(self.bienvenida, False, True, 15)
        self.contenedor_nivel.pack_start(self.imagen_menu, False, True, 15)
        self.contenedor_nivel.pack_start(
            self.contenedor_nivel_h, True, True, 0)
        self.contenedor_nivel_h.pack_start(
            self.contenedor_nivel_1, True, True, 20)
        self.contenedor_nivel_h.pack_start(
            self.contenedor_nivel_2, True, True, 20)
        self.contenedor_nivel_1.pack_start(self.nivel_1, False, True, 10)
        self.contenedor_nivel_1.pack_start(self.nivel_2, False, True, 10)
        self.contenedor_nivel_1.pack_start(self.nivel_3, False, True, 10)
        self.contenedor_nivel_1.pack_start(self.nivel_4, False, True, 10)
        self.contenedor_nivel_1.pack_start(
            self.cambiar_personaje_btn, False, True, 10)
        self.contenedor_nivel_1.pack_start(self.instrucciones, False, True, 10)
        self.contenedor_nivel_2.pack_start(self.nivel_5, False, True, 10)
        self.contenedor_nivel_2.pack_start(self.nivel_6, False, True, 10)
        self.contenedor_nivel_2.pack_start(self.nivel_7, False, True, 10)
        self.contenedor_nivel_2.pack_start(
            self.nuevapalabra_btn, False, True, 10)
        self.contenedor_nivel_2.pack_start(self.importar_btn, False, True, 10)
        self.contenedor_nivel_2.pack_start(
            self.categoria_libre, False, True, 10)
        self.contenedor_nivel.show_all()

        # interface juego
        self.imagen = Gtk.Image()
        self.instrucciones_label = Gtk.Label()
        # self.instrucciones_label.set_justify(Gtk.Justification.FILL)
        self.instrucciones_label.modify_font(self.modificar_text)
        # self.aciertos_label = Gtk.Label(label=_('Puntaje: 0'))
        self.errores_label = Gtk.Label()
        self.errores_label_2 = Gtk.Label()
        self.errores_label_2.modify_font(self.modificar_text)
        self.palabra_label = Gtk.Label()
        self.definicion_label = Gtk.Label()
        self.definicion_label.modify_font(self.modificar_text)
        self.definicion = Gtk.Label()
        self.definicion.set_line_wrap(True)
        self.pista_label = Gtk.Label()
        self.pista_label.modify_font(self.modificar_text)
        self.pista = Gtk.Label()
        self.pista.set_line_wrap(True)
        self.pista.set_max_width_chars(30)
        self.letrasusadas_label = Gtk.Label()
        self.letrasusadas_label_2 = Gtk.Label()
        self.letrasusadas_label_2.modify_font(self.modificar_text)
        self.palabra_entry = Gtk.Entry()
        self.ok_btn = Gtk.Button(_('Ingresar'))
        self.ok_btn.connect('clicked', self._ok_btn_clicked_cb, None)
        self.nuevojuego_btn = Gtk.Button(_('Nuevo Juego'))
        self.nuevojuego_btn.connect(
            'clicked', self._nuevojuego_btn_clicked_cb, None)
        self.atras_btn = Gtk.Button(_('Atrás'))
        self.atras_btn.connect('clicked', self._atras_cb)
        # Cuenta los aciertos de letras en la palabra secreta
        self.aciertos = 0

        # agregando elementos juego
        self.marco = Gtk.Frame(label="Instrucciones")
        self.marco.set_size_request(350, -1)
        self.contenedor_superior.pack_start(self.imagen, True, True, 0)
        self.contenedor_superior.pack_start(self.marco, True, True, 0)

        self.subcontenedor.pack_start(self.instrucciones_label, True, True, 0)
        self.subcontenedor.pack_start(self.definicion_label, False, True, 5)
        self.subcontenedor.pack_start(self.definicion, False, True, 5)
        self.subcontenedor.pack_start(self.pista_label, False, True, 5)
        self.subcontenedor.pack_start(self.pista, False, True, 5)
        # self.subcontenedor.pack_start(self.aciertos_label, True, True, 0)
        self.subcontenedor.pack_start(self.errores_label_2, False, True, 5)
        self.subcontenedor.pack_start(self.errores_label, False, True, 5)
        self.subcontenedor.pack_start(
            self.letrasusadas_label_2, False, True, 0)
        self.subcontenedor.pack_start(self.letrasusadas_label, False, True, 0)
        self.subcontenedor.pack_start(self.palabra_label, True, True, 0)
        self.marco.add(self.subcontenedor)

        self.contenedor_inferior.pack_start(self.atras_btn, False, True, 6)
        self.contenedor_inferior.pack_start(self.palabra_entry, True, True, 1)
        self.contenedor_inferior.pack_start(self.ok_btn, False, True, 1)
        self.contenedor_inferior.pack_start(
            self.nuevojuego_btn, False, True, 1)

        # interface instrucciones
        self.area_instruc = Gtk.ScrolledWindow()
        self.area_instruc.set_shadow_type(Gtk.ShadowType.OUT)
        self.area_instruc.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
        self.imagen_1 = Gtk.Image()
        self.imagen_1.set_from_file('resources/sindiente1.png')
        self.imagen_2 = Gtk.Image()
        self.imagen_2.set_from_file('resources/sindiente2.png')
        self.imagen_3 = Gtk.Image()
        self.imagen_3.set_from_file('resources/sindiente3.png')
        self.imagen_4 = Gtk.Image()
        self.imagen_4.set_from_file('resources/sindiente4.png')

        self.instruc = Gtk.Label(label=_('Instrucciones'))
        self.instruc.modify_font(self.modificar_text)
        self.instruc_1 = Gtk.Label(
            label=_('Oprime el botón “Nuevo Juego” para empezar a \njugar.'))
        self.instruc_2 = Gtk.Label(label=_(
            'La lineas representan las letras de las palabras \nque están ocultas.\
             Cuenta las letras se compone \nla palabra.'))
        self.instruc_3 = Gtk.Label(label=_(
            'Ingresa una letra en el espacio en blanco y oprime\
             \nel botón “Ingresar”.Si descubres una letra esta\
             \naparecerá sobre la linea y ganarás un punto.\
             \nPero si fallas, tu amigo perderá un diente.'))
        self.instruc_4 = Gtk.Label(label=_(
            'Las letras que ya han sido ingresadas no podrán ser \nusada\
             de nuevo y aparecerán en el área de "Letras Usadas"'))
        self.atras_btn_1 = Gtk.Button(_('Atrás'))
        self.atras_btn_1.connect('clicked', self._atras_cb)

        # agregando elementos de instrucciones
        self.contenedor_instruc_1.pack_start(self.instruc_1, True, True, 0)
        self.contenedor_instruc_1.pack_start(self.imagen_1, True, True, 0)
        self.contenedor_instruc_2.pack_start(self.imagen_2, True, True, 0)
        self.contenedor_instruc_2.pack_start(self.instruc_2, True, True, 0)
        self.contenedor_instruc_3.pack_start(self.instruc_3, True, True, 0)
        self.contenedor_instruc_3.pack_start(self.imagen_3, True, True, 0)
        self.contenedor_instruc_4.pack_start(self.imagen_4, True, True, 0)
        self.contenedor_instruc_4.pack_start(self.instruc_4, True, True, 0)
        self.contenedor_instruc.pack_start(self.instruc, True, True, 25)
        self.contenedor_instruc.pack_start(
            self.contenedor_instruc_1, True, True, 50)
        self.contenedor_instruc.pack_start(
            self.contenedor_instruc_2, True, True, 50)
        self.contenedor_instruc.pack_start(
            self.contenedor_instruc_3, True, True, 50)
        self.contenedor_instruc.pack_start(
            self.contenedor_instruc_4, True, True, 15)
        self.contenedor_instruc.pack_start(self.atras_btn_1, True, True, 0)
        self.area_instruc.add_with_viewport(self.contenedor_instruc)

        # interface nueva palabra
        self.nueva_palabra_label = Gtk.Label(
            label=_('Ingresa una palabra para jugar'))
        self.nueva_palabra_label.modify_font(self.modificar_text)
        self.n_palabra_label = Gtk.Label(label=_('Palabra'))
        self.nuevo_significado_label = Gtk.Label(label=_('Significado'))
        self.nueva_pista_label = Gtk.Label(label=_('Pista'))
        self.nueva_palabra = Gtk.Entry()
        self.nuevo_significado = Gtk.Entry()
        self.nueva_pista = Gtk.Entry()
        self.boton_np = Gtk.Button(_('Ingresar palabra'))
        self.boton_np.connect('clicked', self._nueva_p_cb)
        self.atras_imp = Gtk.Button(_('Atrás'))
        self.atras_imp.connect('clicked', self._atras_cb)

        # agregando elementos de nueva palabra
        self.contenedor_np_v.pack_start(
            self.nueva_palabra_label, False, True, 80)
        self.contenedor_np_v.pack_start(self.n_palabra_label, False, True, 0)
        self.contenedor_np_v.pack_start(self.nueva_palabra, False, True, 15)
        self.contenedor_np_v.pack_start(self.nueva_pista_label, False, True, 0)
        self.contenedor_np_v.pack_start(self.nueva_pista, False, True, 15)
        self.contenedor_np_v.pack_start(
            self.nuevo_significado_label, False, True, 0)
        self.contenedor_np_v.pack_start(
            self.nuevo_significado, False, True, 15)
        self.contenedor_np_v.pack_start(
            self.contenedor_np_1, False, False, 100)
        self.contenedor_np_1.pack_start(self.atras_imp, True, False, 0)
        self.contenedor_np_1.pack_start(self.boton_np, True, False, 0)
        self.contenedor_np_2.pack_start(self.contenedor_np_v, True, True, 100)

        # interface importar
        self.combo = self.combo = Gtk.ComboBoxText()
        self.combo.set_size_request(180, -1)
        self.combo.append_text(palabras_nivel_1[0])
        self.combo.append_text(palabras_nivel_2[0])
        self.combo.append_text(palabras_nivel_3[0])
        self.combo.append_text(palabras_nivel_4[0])
        self.combo.append_text(palabras_nivel_5[0])
        self.combo.append_text(palabras_nivel_6[0])
        self.combo.append_text(palabras_nivel_7[0])
        self.combo.append_text(_('Categoría Personalizada'))
        self.combo.set_active(0)
        self.atras_btn_imp = Gtk.Button(_('Atrás'))
        self.atras_btn_imp.connect('clicked', self._atras_cb)
        self.boton_importar = Gtk.Button(_('Importar'))
        self.boton_importar.connect('clicked', self._importar_archivo_cb)
        self.archivo = Gtk.FileChooserWidget()
        self.archivo.set_current_folder('/media')
        self.niveles = Gtk.Label(label=_('Categorías'))
        self.importar = Gtk.HBox()
        self.importar.pack_start(self.atras_btn_imp, False, True, 5)
        self.importar.pack_start(self.niveles, False, True, 10)
        self.importar.pack_start(self.combo, False, True, 0)
        self.importar.pack_start(self.boton_importar, True, True, 0)
        self.archivo.set_extra_widget(self.importar)

        # interface categoria personalizada NONE

        self.lab = Gtk.Label(label=_(
            'No se ha importado ninguna lista de palabras\
             para crear una categoría personalizada'))
        self.atras_btn_fix = Gtk.Button(_('Atrás'))
        self.atras_btn_fix.connect('clicked', self._atras_cb)
        self.sin_importar = Gtk.VBox()
        self.sin_importar.pack_start(self.lab, False, True, 250)
        self.sin_importar.pack_start(self.atras_btn_fix, False, True, 50)

        self.show()

    def _archivo_sugar(self):
        '''copia los archivos'''
        ruta = self.sugar_data + 'nivel1.palabra'
        if not os.path.exists(ruta):  # ningun archivo copiado aún
            for i in range(1, 8):
                ruta = self.sugar_data + 'nivel%s.palabra' % i
                _logger.debug(ruta)
                ruta_origen = 'resources/nivel%s.palabra' % i
                _logger.debug(ruta_origen)
                origen = open(ruta_origen, 'r')
                contenido = origen.read()
                destino = open(ruta, 'w')
                destino.write(contenido)
                destino.close()
                origen.close()
        else:
            pass

    def _crear_interfaz_normal(self):
        '''crea la interfaz de juego'''
        self.ok_btn.set_sensitive(False)
        self.palabra_entry.set_sensitive(False)
        self._cambiar_imagen(0)
        if self.comprobar_interfaz:
            self.contenedor_inferior.remove(self.nuevojuego_imp)
            self.contenedor_inferior.pack_start(
                self.nuevojuego_btn, False, True, 1)
            self.comprobar_interfaz = False

    def _crear_interfaz_personalidad(self):
        '''
        crea la interfaz cuando se quire ingresar una palabra personalizada
        '''
        if self.comprobar_interfaz is not True:
            self._cambiar_imagen(0)
            self.nuevojuego_imp = Gtk.Button(_('Nuevo juego'))
            self.nuevojuego_imp.connect('clicked', self._nuevo_juegoimp_cb)
            self.contenedor_inferior.remove(self.nuevojuego_btn)
            self.contenedor_inferior.pack_start(
                self.nuevojuego_imp, False, True, 1)
        self.comprobar_interfaz = True

    def _creacion(self, nuevo=True, custom=False):
        '''Crea las variables necesarias para el comienzo del juego'''
        if nuevo:
            if custom:
                self.palabra = self.nueva_palabra.get_text()
                self.texto_pista = self.nueva_pista.get_text()
                self.significado = self.nuevo_significado.get_text()
            else:
                contenido = utils.palabra_aleatoria(
                    self.sugar_data, self.nivel)
                _logger.warning(contenido)
                self.palabra = unicode(contenido[0], "utf-8")
                self.texto_pista = contenido[1]
                self.significado = contenido[2]

            self.l_aciertos = []
            self.l_errores = []
            self.errores = 0
            self._cambiar_imagen(0)
        else:
            self._cambiar_imagen(self.errores)

        self._actualizar_labels(_('El juego ha empezado'))
        self._pintar_palabra()

    def _limpiar(self):
        '''limpia pantalla'''
        self.palabra_entry.set_sensitive(False)
        self.ok_btn.set_sensitive(False)
        self.pista_label.set_text('')
        self.pista.set_text('')
        self.definicion_label.set_text('')
        self.definicion.set_text('')
        self.instrucciones_label.set_text('')
        self.palabra_label.set_text('')
        self.errores_label.set_text('')
        self.errores_label_2.set_text('')
        self.letrasusadas_label.set_text('')
        self.letrasusadas_label_2.set_text('')
        self._cambiar_imagen(0)

    # callbacks

    def _btn_nino_1_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '1/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _btn_nino_2_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '2/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _btn_nino_3_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '3/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _btn_nina_1_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '4/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _btn_nina_2_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '5/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _btn_nina_3_cb(self, widget, data=None):
        self.ruta_imagen = self.carpeta_imagen + '6/'
        self.imagen_menu.set_from_file(self.ruta_imagen + '00.png')
        self.set_canvas(self.contenedor_nivel)

    def _atras_cb(self, widget, data=None):
        self.set_canvas(self.contenedor_nivel)
        self._limpiar()

    def _nivel_uno_cb(self, widget, data=None):
        self.nivel = 1
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_dos_cb(self, widget, data=None):
        self.nivel = 2
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_tres_cb(self, widget, data=None):
        self.nivel = 3
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_cuatro_cb(self, widget, data=None):
        self.nivel = 4
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_cinco_cb(self, widget, data=None):
        self.nivel = 5
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_seis_cb(self, widget, data=None):
        self.nivel = 6
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _nivel_siete_cb(self, widget, data=None):
        self.nivel = 7
        self._crear_interfaz_normal()
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)

    def _categoria_personalizada_cb(self, widget, data=None):
        self.nivel = utils.categoria_personalizada(self.sugar_data)
        if self.nivel:
            self._crear_interfaz_normal()
            self.contenedor.show_all()
            self.set_canvas(self.contenedor)
        else:
            self.sin_importar.show_all()
            self.set_canvas(self.sin_importar)
            # pass #mostrar mensaje

    def _cambiar_personaje_cb(self, widget, data=None):
        self.set_canvas(self.elegir_personaje_v)

    def _instrucciones_cb(self, widget, data=None):
        self.area_instruc.show_all()
        self.set_canvas(self.area_instruc)

    def _importar_cb(self, widget, data=None):
        '''callback del menu'''
        self.archivo.show_all()
        self.set_canvas(self.archivo)

    def _importar_archivo_cb(self, widget, data=None):
        '''importa una nueva lista de palabras'''
        self.modelocombo = self.combo.get_model()
        self.nivel = self.combo.get_active()
        self.uri = self.archivo.get_uri()
        self.uri = self.uri[7:]
        utils.importar_lista_p(self.sugar_data, self.uri, self.nivel)

    def _nuevapalabra_cb(self, widget, data=None):
        '''callback del menu'''
        self.contenedor_np_2.show_all()
        self.set_canvas(self.contenedor_np_2)

    def _nueva_p_cb(self, widget, data=None):
        '''ingresar nueva palabra'''
        self._crear_interfaz_personalidad()
        self._creacion(custom=True)
        self.contenedor.show_all()
        self.set_canvas(self.contenedor)
        self.palabra_entry.set_sensitive(True)
        self.ok_btn.set_sensitive(True)
        self.nuevojuego_btn.set_sensitive(True)
        self.nueva_palabra.set_text('')
        self.nuevo_significado.set_text('')
        self.nueva_pista.set_text('')

    def _nuevo_juegoimp_cb(self, widget, data=None):
        '''nuevo juego en la interfaz de juego personalizado'''
        self.contenedor_np_2.show_all()
        self.set_canvas(self.contenedor_np_2)

    def _ok_btn_clicked_cb(self, widget, data=None):
        self._actualizar_palabra()

    def _nuevojuego_btn_clicked_cb(self, widget, data=None):
        self.palabra_entry.set_sensitive(True)  # Activa la caja de texto
        self.ok_btn.set_sensitive(True)  # Activa el botón ok
        self.aciertos = 0
        self._creacion()

    def _cambiar_imagen(self, level):
        ruta = self.ruta_imagen + '%s.png' % level
        self.imagen.set_from_file(ruta)

    def _key_press_cb(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == "KP_Enter":

            self._actualizar_palabra()
        return False

    def _actualizar_palabra(self):

        # Convierte la letra a minuscula
        letra_actual = self.palabra_entry.get_text().lower()
        letra_actual = unicode(letra_actual, "utf-8")
        # Divive en dos palabras
        if ' ' in self.palabra:
            longitud_palabra = len(self.palabra) - 1
        else:
            longitud_palabra = len(self.palabra)

        _logger.debug(letra_actual)
        # Evalua si se escribio mas de 1 letra o esta vacio
        if (len(letra_actual) is not 1 or letra_actual == " "):
            self.palabra_entry.set_text('')
            self.instrucciones_label.set_text(_("Introduzca solo una letra!"))

        # Evalua si letra esta dentro de palabra
        elif (letra_actual in self.palabra
                and letra_actual not in self.l_aciertos):
            self.l_aciertos.append(letra_actual)
            for i in range(len(self.palabra)):
                if letra_actual == self.palabra[i] and self.palabra[i] != ' ':
                    self.aciertos += 1
                    _logger.debug(self.aciertos)

            self._actualizar_labels("Letra dentro de palabra secreta!")

            # Evalua si se acerto la palabra y temina el juego
            if self.aciertos == longitud_palabra:
                self.instrucciones_label.set_text(
                    _('FELICIDADES!\nAcertastes la palabra secreta'))
                self.definicion_label.set_text(_('Significado:'))
                self.definicion.set_text(_(self.significado))
                self.palabra_entry.set_sensitive(False)
                self.ok_btn.set_sensitive(False)
                self.aciertos = 0
                # self.nuevojuego_btn.show() # muestra el boton para comenzar
                # el juego

        # Evalua si letra es repetida y esta dentro de palabra
        elif (letra_actual in self.palabra
                and letra_actual in self.l_aciertos):
            self._actualizar_labels(
                "Letra repetida y dentro de palabra secreta!")

        # Evalua si letra no esta dentro de palabra
        elif (letra_actual not in self.palabra
                and letra_actual not in self.l_errores):
            self.l_errores.append(letra_actual)
            self.errores += 1
            self._cambiar_imagen(self.errores)
            self._actualizar_labels("Letra fuera de palabra secreta!")

            # Evalua si se completo el ahorcado y temina el juego
            if (self.errores >= 8):
                self.instrucciones_label.set_text(_(
                    'Fin de Juego\nLa palabra secreta era %s' % self.palabra))
                self.definicion_label.set_text(_('Significado:'))
                self.definicion.set_text(_(self.significado))
                self.aciertos = 0
                self.palabra_entry.set_sensitive(
                    False)  # Activa la caja de texto
                # Inactiva el botón ok una vez que pierde
                self.ok_btn.set_sensitive(False)

        # Evalua si letra es repetida y no dentro de palabra
        elif (letra_actual not in self.palabra
                and letra_actual in self.l_errores):
            self._actualizar_labels(
                "Letra repetida y fuera de palabra secreta!")

        self._pintar_palabra()

    def _actualizar_labels(self, instrucciones):
        '''Actualiza labels segun instrucciones'''
        self.palabra_entry.set_text('')
        self.pista_label.set_text(_('Pista:'))
        self.pista.set_text(self.texto_pista)
        self.definicion_label.set_text('')
        self.definicion.set_text('')
        self.instrucciones_label.set_text(_(instrucciones))
        # self.aciertos_label.set_text(_('Puntaje: %s' % self.aciertos))
        letras = ', '.join(letra for letra in self.l_aciertos)
        letras2 = ', '.join(letra for letra in self.l_errores)
        self.letrasusadas_label_2.set_text(_('Letras usadas:'))
        self.letrasusadas_label.set_text('%s %s' % (letras, letras2))
        self.errores_label_2.set_text(_('Errores:'))
        self.errores_label.set_text('%s' % self.errores)

    def _pintar_palabra(self):
        '''Pinta las lineas de la palabra'''
        pista = ''
        for letra in self.palabra:
            if letra in self.l_aciertos:
                pista += '%s ' % letra
            elif letra != ' ':  # no pintar espacios
                pista += '_ '
            else:
                pista += ' '
        self.palabra_label.set_text(pista)

    def read_file(self, filepath):
        pass

    def write_file(self, filepath):
        pass

    def close(self, skip_save=False):
        '''override the close to jump the journal'''
        activity.Activity.close(self, True)
