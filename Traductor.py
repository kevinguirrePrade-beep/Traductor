import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import pickle
from enum import Enum
from datetime import datetime
import os

class Idioma(Enum):
    INGLES = "inglés"
    ESPANOL = "español"
    FRANCES = "francés"
    PORTUGUES = "portugués"

class Traduccion:
    def __init__(self, texto_traduccion):
        self.texto = texto_traduccion
        self.puntuacion_promedio = 5.0
        self.total_evaluaciones = 1
        self.historial_puntuaciones = [5.0]
        self.fecha_creacion = datetime.now()
        self.fecha_ultima_modificacion = datetime.now()
    
    def actualizar_puntuacion(self, nueva_puntuacion):
        self.historial_puntuaciones.append(nueva_puntuacion)
        self.total_evaluaciones += 1
        self.puntuacion_promedio = sum(self.historial_puntuaciones) / self.total_evaluaciones
        self.fecha_ultima_modificacion = datetime.now()
    
    def to_dict(self):
        return {
            'texto': self.texto,
            'puntuacion_promedio': self.puntuacion_promedio,
            'total_evaluaciones': self.total_evaluaciones,
            'historial_puntuaciones': self.historial_puntuaciones,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_ultima_modificacion': self.fecha_ultima_modificacion.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        traduccion = cls(data['texto'])
        traduccion.puntuacion_promedio = data['puntuacion_promedio']
        traduccion.total_evaluaciones = data['total_evaluaciones']
        traduccion.historial_puntuaciones = data['historial_puntuaciones']
        traduccion.fecha_creacion = datetime.fromisoformat(data['fecha_creacion'])
        traduccion.fecha_ultima_modificacion = datetime.fromisoformat(data['fecha_ultima_modificacion'])
        return traduccion

class TraductorAprendizaje:
    """Clase del traductor con capacidad de fusionar diccionarios"""
    def __init__(self):
        self.diccionario = {}
        self.historial_traducciones = []
        self.inicializar_diccionario()
        self.inicializar_traducciones()
    
    def inicializar_diccionario(self):
        for idioma_origen in Idioma:
            self.diccionario[idioma_origen] = {}
            for idioma_destino in Idioma:
                if idioma_origen != idioma_destino:
                    self.diccionario[idioma_origen][idioma_destino] = {}
    
    def inicializar_traducciones(self):
        """Agrega traducciones iniciales al diccionario (con puntuación por defecto 5)"""
        # Español -> Inglés
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.INGLES, "hola", "hello")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.INGLES, "adiós", "goodbye")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.INGLES, "gracias", "thank you")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.INGLES, "por favor", "please")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.INGLES, "agua", "water")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.INGLES, "comida", "food")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.INGLES, "casa", "house")
        
        # Inglés -> Español
        self.agregar_traduccion(Idioma.INGLES, Idioma.ESPANOL, "hello", "hola")
        self.agregar_traduccion(Idioma.INGLES, Idioma.ESPANOL, "goodbye", "adiós")
        self.agregar_traduccion(Idioma.INGLES, Idioma.ESPANOL, "thank you", "gracias")
        self.agregar_traduccion(Idioma.INGLES, Idioma.ESPANOL, "please", "por favor")
        self.agregar_traduccion(Idioma.INGLES, Idioma.ESPANOL, "water", "agua")
        self.agregar_traduccion(Idioma.INGLES, Idioma.ESPANOL, "food", "comida")
        self.agregar_traduccion(Idioma.INGLES, Idioma.ESPANOL, "house", "casa")
        
        # Español -> Francés
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.FRANCES, "hola", "bonjour")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.FRANCES, "adiós", "au revoir")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.FRANCES, "gracias", "merci")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.FRANCES, "agua", "eau")
        
        # Francés -> Español
        self.agregar_traduccion(Idioma.FRANCES, Idioma.ESPANOL, "bonjour", "hola")
        self.agregar_traduccion(Idioma.FRANCES, Idioma.ESPANOL, "au revoir", "adiós")
        self.agregar_traduccion(Idioma.FRANCES, Idioma.ESPANOL, "merci", "gracias")
        self.agregar_traduccion(Idioma.FRANCES, Idioma.ESPANOL, "eau", "agua")
        
        # Español -> Portugués
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.PORTUGUES, "hola", "olá")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.PORTUGUES, "adiós", "adeus")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.PORTUGUES, "gracias", "obrigado")
        self.agregar_traduccion(Idioma.ESPANOL, Idioma.PORTUGUES, "agua", "água")
        
        # Portugués -> Español
        self.agregar_traduccion(Idioma.PORTUGUES, Idioma.ESPANOL, "olá", "hola")
        self.agregar_traduccion(Idioma.PORTUGUES, Idioma.ESPANOL, "adeus", "adiós")
        self.agregar_traduccion(Idioma.PORTUGUES, Idioma.ESPANOL, "obrigado", "gracias")
        self.agregar_traduccion(Idioma.PORTUGUES, Idioma.ESPANOL, "água", "agua")
        
        # Inglés -> Francés
        self.agregar_traduccion(Idioma.INGLES, Idioma.FRANCES, "hello", "bonjour")
        self.agregar_traduccion(Idioma.INGLES, Idioma.FRANCES, "goodbye", "au revoir")
        self.agregar_traduccion(Idioma.INGLES, Idioma.FRANCES, "water", "eau")
        
        # Inglés -> Portugués
        self.agregar_traduccion(Idioma.INGLES, Idioma.PORTUGUES, "hello", "olá")
        self.agregar_traduccion(Idioma.INGLES, Idioma.PORTUGUES, "goodbye", "adeus")
        self.agregar_traduccion(Idioma.INGLES, Idioma.PORTUGUES, "water", "água")
    
    def fusionar_traduccion(self, origen, destino, texto_origen, nueva_traduccion):
        """
        Fusiona una traducción: si ya existe, combina las estadísticas
        Si no existe, la agrega
        """
        texto_origen_lower = texto_origen.lower()
        
        
        existe = (origen in self.diccionario and 
                destino in self.diccionario[origen] and
                texto_origen_lower in self.diccionario[origen][destino])
        
        if existe:
            existente = self.diccionario[origen][destino][texto_origen_lower]
            
            if existente.texto != nueva_traduccion.texto:
                existente.texto = nueva_traduccion.texto
            
            historial_combinado = existente.historial_puntuaciones + nueva_traduccion.historial_puntuaciones
            existente.historial_puntuaciones = historial_combinado
            existente.total_evaluaciones = len(historial_combinado)
            existente.puntuacion_promedio = sum(historial_combinado) / existente.total_evaluaciones
            
            existente.fecha_ultima_modificacion = datetime.now()
            
            return "actualizada"
        else:
            if origen not in self.diccionario:
                self.diccionario[origen] = {}
            if destino not in self.diccionario[origen]:
                self.diccionario[origen][destino] = {}
            
            self.diccionario[origen][destino][texto_origen_lower] = nueva_traduccion
            return "agregada"
    
    def fusionar_diccionario_completo(self, nuevo_diccionario, nuevo_historial):
        """
        Fusiona un diccionario completo con el existente
        Devuelve estadísticas de la fusión
        """
        estadisticas = {
            'total_traducciones_antes': self.obtener_total_traducciones(),
            'traducciones_agregadas': 0,
            'traducciones_actualizadas': 0,
            'errores': 0
        }
        
        for origen, destinos in nuevo_diccionario.items():
            for destino, traducciones in destinos.items():
                for texto_origen, nueva_traduccion in traducciones.items():
                    try:
                        resultado = self.fusionar_traduccion(origen, destino, texto_origen, nueva_traduccion)
                        if resultado == "agregada":
                            estadisticas['traducciones_agregadas'] += 1
                        elif resultado == "actualizada":
                            estadisticas['traducciones_actualizadas'] += 1
                    except Exception as e:
                        estadisticas['errores'] += 1
                        print(f"Error fusionando traducción: {e}")
        
        if nuevo_historial:
            self.historial_traducciones.extend(nuevo_historial)
            self.historial_traducciones.sort(key=lambda x: x['fecha'])
        
        estadisticas['total_traducciones_despues'] = self.obtener_total_traducciones()
        return estadisticas
    
    def obtener_total_traducciones(self):
        """Obtiene el número total de traducciones en el diccionario"""
        total = 0
        for destinos in self.diccionario.values():
            for traducciones in destinos.values():
                total += len(traducciones)
        return total
    
    def agregar_traduccion(self, idioma_origen, idioma_destino, texto_origen, texto_traduccion):
        """Agrega una traducción con puntuación inicial por defecto (5)"""
        self.agregar_traduccion_con_puntuacion(idioma_origen, idioma_destino, texto_origen, texto_traduccion, 5)
    
    def agregar_traduccion_con_puntuacion(self, idioma_origen, idioma_destino, texto_origen, texto_traduccion, puntuacion):
        texto_origen_lower = texto_origen.lower()
        
        if idioma_origen not in self.diccionario:
            self.diccionario[idioma_origen] = {}
        if idioma_destino not in self.diccionario[idioma_origen]:
            self.diccionario[idioma_origen][idioma_destino] = {}
        
        nueva_traduccion = Traduccion(texto_traduccion)
        nueva_traduccion.historial_puntuaciones = [puntuacion]
        nueva_traduccion.puntuacion_promedio = puntuacion
        
        self.diccionario[idioma_origen][idioma_destino][texto_origen_lower] = nueva_traduccion
        
        self.historial_traducciones.append({
            'fecha': datetime.now(),
            'accion': 'agregar',
            'origen': idioma_origen,
            'destino': idioma_destino,
            'texto_origen': texto_origen,
            'texto_traduccion': texto_traduccion
        })
    
    def traducir(self, idioma_origen, idioma_destino, texto):
        texto_lower = texto.lower()
        
        if (idioma_origen in self.diccionario and 
            idioma_destino in self.diccionario[idioma_origen] and
            texto_lower in self.diccionario[idioma_origen][idioma_destino]):
            
            traduccion = self.diccionario[idioma_origen][idioma_destino][texto_lower]
            
            self.historial_traducciones.append({
                'fecha': datetime.now(),
                'accion': 'traducir',
                'origen': idioma_origen,
                'destino': idioma_destino,
                'texto_origen': texto,
                'texto_traduccion': traduccion.texto,
                'puntuacion': traduccion.puntuacion_promedio
            })
            
            return traduccion.texto
        
        return None
    
    def existe_traduccion(self, idioma_origen, idioma_destino, texto):
        texto_lower = texto.lower()
        return (idioma_origen in self.diccionario and 
                idioma_destino in self.diccionario[idioma_origen] and
                texto_lower in self.diccionario[idioma_origen][idioma_destino])
    
    def evaluar_traduccion(self, idioma_origen, idioma_destino, texto, puntuacion):
        if puntuacion < 1 or puntuacion > 10:
            return False, "La puntuación debe estar entre 1 y 10"
        
        texto_lower = texto.lower()
        
        if not self.existe_traduccion(idioma_origen, idioma_destino, texto):
            return False, "No existe una traducción para ese texto"
        
        traduccion = self.diccionario[idioma_origen][idioma_destino][texto_lower]
        puntuacion_anterior = traduccion.puntuacion_promedio
        
        traduccion.actualizar_puntuacion(puntuacion)
        
        self.historial_traducciones.append({
            'fecha': datetime.now(),
            'accion': 'evaluar',
            'origen': idioma_origen,
            'destino': idioma_destino,
            'texto_origen': texto,
            'puntuacion': puntuacion,
            'puntuacion_anterior': puntuacion_anterior
        })
        
        mensaje = (f"Evaluación registrada: {puntuacion}/10\n"
                f"Puntuación anterior: {puntuacion_anterior:.1f}/10\n"
                f"Nueva puntuación: {traduccion.puntuacion_promedio:.1f}/10")
        
        return True, mensaje
    
    def obtener_estadisticas(self):
        total_traducciones = 0
        total_evaluaciones = 0
        puntuacion_global = 0
        combinaciones_con_traducciones = 0
        
        estadisticas_idiomas = {}
        
        for idioma in Idioma:
            estadisticas_idiomas[idioma.value] = {
                'como_origen': 0,
                'como_destino': 0,
                'mejor_puntuacion': 0,
                'peor_puntuacion': 10
            }
        
        for idioma_origen in self.diccionario:
            for idioma_destino in self.diccionario[idioma_origen]:
                traducciones = self.diccionario[idioma_origen][idioma_destino]
                
                if traducciones:
                    total_combinacion = len(traducciones)
                    total_traducciones += total_combinacion
                    
                    estadisticas_idiomas[idioma_origen.value]['como_origen'] += total_combinacion
                    estadisticas_idiomas[idioma_destino.value]['como_destino'] += total_combinacion
                    
                    suma_puntuaciones = 0
                    for trad in traducciones.values():
                        suma_puntuaciones += trad.puntuacion_promedio
                        total_evaluaciones += trad.total_evaluaciones
                        
                        if trad.puntuacion_promedio > estadisticas_idiomas[idioma_origen.value]['mejor_puntuacion']:
                            estadisticas_idiomas[idioma_origen.value]['mejor_puntuacion'] = trad.puntuacion_promedio
                        if trad.puntuacion_promedio < estadisticas_idiomas[idioma_origen.value]['peor_puntuacion']:
                            estadisticas_idiomas[idioma_origen.value]['peor_puntuacion'] = trad.puntuacion_promedio
                    
                    promedio_combinacion = suma_puntuaciones / len(traducciones) if traducciones else 0
                    puntuacion_global += promedio_combinacion
                    combinaciones_con_traducciones += 1
        
        puntuacion_global_promedio = puntuacion_global / combinaciones_con_traducciones if combinaciones_con_traducciones > 0 else 0
        
        return {
            'total_traducciones': total_traducciones,
            'total_evaluaciones': total_evaluaciones,
            'puntuacion_global': puntuacion_global_promedio,
            'combinaciones_con_traducciones': combinaciones_con_traducciones,
            'estadisticas_idiomas': estadisticas_idiomas,
            'historial_traducciones': len(self.historial_traducciones)
        }
    
    def obtener_mejores_traducciones(self, idioma_origen, idioma_destino, limite=10):
        if (idioma_origen not in self.diccionario or 
            idioma_destino not in self.diccionario[idioma_origen]):
            return []
        
        traducciones = self.diccionario[idioma_origen][idioma_destino]
        
        lista_traducciones = [
            (texto_origen, trad) 
            for texto_origen, trad in traducciones.items()
        ]
        
        lista_traducciones.sort(key=lambda x: x[1].puntuacion_promedio, reverse=True)
        
        return lista_traducciones[:limite]
    
    def obtener_peores_traducciones(self, idioma_origen, idioma_destino, limite=10):
        if (idioma_origen not in self.diccionario or 
            idioma_destino not in self.diccionario[idioma_origen]):
            return []
        
        traducciones = self.diccionario[idioma_origen][idioma_destino]
        
        lista_traducciones = [
            (texto_origen, trad) 
            for texto_origen, trad in traducciones.items()
        ]
        
        lista_traducciones.sort(key=lambda x: x[1].puntuacion_promedio)
        
        return lista_traducciones[:limite]
    
    def guardar_diccionario_binario(self, archivo):
        try:
            datos_serializables = {}
            
            for idioma_origen in self.diccionario:
                datos_serializables[idioma_origen.value] = {}
                
                for idioma_destino in self.diccionario[idioma_origen]:
                    datos_serializables[idioma_origen.value][idioma_destino.value] = {}
                    
                    for texto, traduccion in self.diccionario[idioma_origen][idioma_destino].items():
                        datos_serializables[idioma_origen.value][idioma_destino.value][texto] = traduccion.to_dict()
            
            historial_serializable = []
            for registro in self.historial_traducciones:
                registro_copy = registro.copy()
                registro_copy['fecha'] = registro_copy['fecha'].isoformat()
                if 'origen' in registro_copy and isinstance(registro_copy['origen'], Idioma):
                    registro_copy['origen'] = registro_copy['origen'].value
                if 'destino' in registro_copy and isinstance(registro_copy['destino'], Idioma):
                    registro_copy['destino'] = registro_copy['destino'].value
                historial_serializable.append(registro_copy)
            
            datos_completos = {
                'diccionario': datos_serializables,
                'historial': historial_serializable,
                'fecha_guardado': datetime.now().isoformat()
            }
            
            with open(archivo, 'wb') as f:
                pickle.dump(datos_completos, f)
            
            return True, f"Diccionario guardado exitosamente en {archivo}"
            
        except Exception as e:
            return False, f"Error al guardar el diccionario: {str(e)}"
    
    def cargar_diccionario_binario(self, archivo, fusionar=True):
        try:
            with open(archivo, 'rb') as f:
                datos_completos = pickle.load(f)
            diccionario_nuevo = {}
            historial_nuevo = []
            
            for idioma_origen_str, destinos in datos_completos['diccionario'].items():
                idioma_origen = None
                for idioma in Idioma:
                    if idioma.value == idioma_origen_str:
                        idioma_origen = idioma
                        break
                
                if idioma_origen is None:
                    continue
                
                diccionario_nuevo[idioma_origen] = {}
                
                for idioma_destino_str, traducciones in destinos.items():
                    idioma_destino = None
                    for idioma in Idioma:
                        if idioma.value == idioma_destino_str:
                            idioma_destino = idioma
                            break
                    
                    if idioma_destino is None:
                        continue
                    
                    diccionario_nuevo[idioma_origen][idioma_destino] = {}
                    
                    for texto, datos_traduccion in traducciones.items():
                        diccionario_nuevo[idioma_origen][idioma_destino][texto] = Traduccion.from_dict(datos_traduccion)
            
            for registro in datos_completos.get('historial', []):
                registro_copy = registro.copy()
                registro_copy['fecha'] = datetime.fromisoformat(registro_copy['fecha'])
                
                if 'origen' in registro_copy and isinstance(registro_copy['origen'], str):
                    for idioma in Idioma:
                        if idioma.value == registro_copy['origen']:
                            registro_copy['origen'] = idioma
                            break
                
                if 'destino' in registro_copy and isinstance(registro_copy['destino'], str):
                    for idioma in Idioma:
                        if idioma.value == registro_copy['destino']:
                            registro_copy['destino'] = idioma
                            break
                
                historial_nuevo.append(registro_copy)
            
            if fusionar:
                estadisticas = self.fusionar_diccionario_completo(diccionario_nuevo, historial_nuevo)
                
                mensaje = (f"Diccionario fusionado exitosamente desde {archivo}\n\n"
                        f"Estadísticas de fusión:\n"
                        f"• Traducciones antes: {estadisticas['total_traducciones_antes']}\n"
                        f"• Traducciones agregadas: {estadisticas['traducciones_agregadas']}\n"
                        f"• Traducciones actualizadas: {estadisticas['traducciones_actualizadas']}\n"
                        f"• Traducciones después: {estadisticas['total_traducciones_despues']}\n"
                        f"• Errores: {estadisticas['errores']}")
                
                return True, mensaje
            else:
                self.diccionario = diccionario_nuevo
                self.historial_traducciones = historial_nuevo
                return True, f"Diccionario reemplazado exitosamente desde {archivo}"
            
        except FileNotFoundError:
            return False, f"Archivo no encontrado: {archivo}"
        except Exception as e:
            return False, f"Error al cargar el diccionario: {str(e)}"
    
    def guardar_diccionario_json(self, archivo):
        try:
            datos_serializables = {}
            
            for idioma_origen in self.diccionario:
                datos_serializables[idioma_origen.value] = {}
                
                for idioma_destino in self.diccionario[idioma_origen]:
                    datos_serializables[idioma_origen.value][idioma_destino.value] = {}
                    
                    for texto, traduccion in self.diccionario[idioma_origen][idioma_destino].items():
                        datos_serializables[idioma_origen.value][idioma_destino.value][texto] = traduccion.to_dict()
            
            historial_serializable = []
            for registro in self.historial_traducciones:
                registro_copy = registro.copy()
                registro_copy['fecha'] = registro_copy['fecha'].isoformat()
                if 'origen' in registro_copy and isinstance(registro_copy['origen'], Idioma):
                    registro_copy['origen'] = registro_copy['origen'].value
                if 'destino' in registro_copy and isinstance(registro_copy['destino'], Idioma):
                    registro_copy['destino'] = registro_copy['destino'].value
                historial_serializable.append(registro_copy)
            
            datos_completos = {
                'diccionario': datos_serializables,
                'historial': historial_serializable,
                'fecha_guardado': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, ensure_ascii=False, indent=2)
            
            return True, f"Diccionario guardado en formato JSON en {archivo}"
            
        except Exception as e:
            return False, f"Error al guardar el diccionario JSON: {str(e)}"
    
    def cargar_diccionario_json(self, archivo, fusionar=True):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos_completos = json.load(f)
            
            diccionario_nuevo = {}
            historial_nuevo = []
            
            for idioma_origen_str, destinos in datos_completos['diccionario'].items():
                idioma_origen = None
                for idioma in Idioma:
                    if idioma.value == idioma_origen_str:
                        idioma_origen = idioma
                        break
                
                if idioma_origen is None:
                    continue
                
                diccionario_nuevo[idioma_origen] = {}
                
                for idioma_destino_str, traducciones in destinos.items():
                    idioma_destino = None
                    for idioma in Idioma:
                        if idioma.value == idioma_destino_str:
                            idioma_destino = idioma
                            break
                    
                    if idioma_destino is None:
                        continue
                    
                    diccionario_nuevo[idioma_origen][idioma_destino] = {}
                    
                    for texto, datos_traduccion in traducciones.items():
                        diccionario_nuevo[idioma_origen][idioma_destino][texto] = Traduccion.from_dict(datos_traduccion)
            
            if 'historial' in datos_completos:
                for registro in datos_completos['historial']:
                    registro_copy = registro.copy()
                    registro_copy['fecha'] = datetime.fromisoformat(registro_copy['fecha'])
                    
                    if 'origen' in registro_copy and isinstance(registro_copy['origen'], str):
                        for idioma in Idioma:
                            if idioma.value == registro_copy['origen']:
                                registro_copy['origen'] = idioma
                                break
                    
                    if 'destino' in registro_copy and isinstance(registro_copy['destino'], str):
                        for idioma in Idioma:
                            if idioma.value == registro_copy['destino']:
                                registro_copy['destino'] = idioma
                                break
                    
                    historial_nuevo.append(registro_copy)
            
            if fusionar:
                estadisticas = self.fusionar_diccionario_completo(diccionario_nuevo, historial_nuevo)
                
                mensaje = (f"Diccionario fusionado exitosamente desde JSON: {archivo}\n\n"
                        f"Estadísticas de fusión:\n"
                        f"• Traducciones antes: {estadisticas['total_traducciones_antes']}\n"
                        f"• Traducciones agregadas: {estadisticas['traducciones_agregadas']}\n"
                        f"• Traducciones actualizadas: {estadisticas['traducciones_actualizadas']}\n"
                        f"• Traducciones después: {estadisticas['total_traducciones_despues']}\n"
                        f"• Errores: {estadisticas['errores']}")
                
                return True, mensaje
            else: 
                self.diccionario = diccionario_nuevo
                self.historial_traducciones = historial_nuevo
                return True, f"Diccionario reemplazado desde JSON: {archivo}"
            
        except FileNotFoundError:
            return False, f"Archivo no encontrado: {archivo}"
        except json.JSONDecodeError:
            return False, f"Error en el formato JSON del archivo: {archivo}"
        except Exception as e:
            return False, f"Error al cargar el diccionario JSON: {str(e)}"
    
    def exportar_traducciones_texto(self, archivo):
        try:
            estadisticas = self.obtener_estadisticas()
            
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("DICCIONARIO DE TRADUCCIONES - TRADUCTOR CON APRENDIZAJE\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de traducciones: {estadisticas['total_traducciones']}\n")
                f.write(f"Puntuación global promedio: {estadisticas['puntuacion_global']:.2f}/10\n\n")
                
                for idioma_origen in Idioma:
                    for idioma_destino in Idioma:
                        if idioma_origen != idioma_destino:
                            traducciones = self.diccionario.get(idioma_origen, {}).get(idioma_destino, {})
                            
                            if traducciones:
                                f.write(f"\n{idioma_origen.value.upper()} → {idioma_destino.value.upper()}:\n")
                                f.write("-" * 40 + "\n")
                                
                                lista_traducciones = sorted(
                                    traducciones.items(),
                                    key=lambda x: x[1].puntuacion_promedio,
                                    reverse=True
                                )
                                
                                for texto_origen, traduccion in lista_traducciones:
                                    f.write(f"  {texto_origen:20} → {traduccion.texto:20} ")
                                    f.write(f"[{traduccion.puntuacion_promedio:.1f}/10, {traduccion.total_evaluaciones} eval.]\n")
            
            return True, f"Traducciones exportadas a {archivo}"
            
        except Exception as e:
            return False, f"Error al exportar traducciones: {str(e)}"

    def limpiar_diccionario(self):
        """Limpia completamente el diccionario y el historial"""
        self.diccionario = {}
        self.historial_traducciones = []
        self.inicializar_diccionario()
        return True, "Diccionario limpiado exitosamente"

class TraductorAprendizajeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traductor con Aprendizaje Automático")
        self.root.state('zoomed')
        self.root.configure(bg="#f0f0f0")
        self.autosave_file = "autosave_traductor.json"
        self.traductor = TraductorAprendizaje()
        self.cargar_autoguardado()
        self.modo_fusion = tk.BooleanVar(value=True)
        self.setup_icons()
        self.setup_styles()
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def cargar_autoguardado(self):
        """Carga el estado guardado automáticamente"""
        if os.path.exists(self.autosave_file):
            try:
                exito, mensaje = self.traductor.cargar_diccionario_json(self.autosave_file, fusionar=False)
                if exito:
                    print("Autoguardado cargado:", mensaje)
                else:
                    print("Error al cargar autoguardado:", mensaje)
            except Exception as e:
                print("Error inesperado al cargar autoguardado:", e)
    
    def guardar_autoguardado(self):
        """Guarda el estado actual en el archivo de autoguardado"""
        try:
            exito, mensaje = self.traductor.guardar_diccionario_json(self.autosave_file)
            if exito:
                print("Autoguardado realizado:", mensaje)
            else:
                print("Error al guardar autoguardado:", mensaje)
        except Exception as e:
            print("Error inesperado al guardar autoguardado:", e)
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.guardar_autoguardado()
        self.root.destroy()
    
    def setup_icons(self):
        """Configurar iconos para la interfaz"""
        self.icons = {
            'translate': "🔤",
            'evaluate': "⭐",
            'add': "➕",
            'stats': "📊",
            'best': "🏆",
            'worst': "⚠️",
            'save': "💾",
            'load': "📂",
            'export': "📄",
            'history': "📋",
            'exit': "🚪",
            'merge': "🔄",
            'clear': "🧹"
        }
    
    def setup_styles(self):
        """Configurar estilos para la interfaz"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'background': '#f0f0f0',
            'merge': '#9b59b6'
        }
        
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                        foreground=self.colors['primary'])
        self.style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'),
                        foreground=self.colors['dark'])
        self.style.configure('Primary.TButton', font=('Arial', 10, 'bold'),
                        background=self.colors['secondary'],
                        foreground='white')
        self.style.configure('Success.TButton', font=('Arial', 10, 'bold'),
                        background=self.colors['success'],
                        foreground='white')
        self.style.configure('Warning.TButton', font=('Arial', 10, 'bold'),
                        background=self.colors['warning'],
                        foreground='white')
        self.style.configure('Merge.TButton', font=('Arial', 10, 'bold'),
                        background=self.colors['merge'],
                        foreground='white')
        
        self.style.configure('Treeview', font=('Arial', 10))
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def setup_ui(self):
        """Configurar la interfaz de usuario principal"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        title_label = ttk.Label(main_frame, text="🌍 Traductor con Aprendizaje Automático", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, 
                                text="Sistema que aprende de tus traducciones y evaluaciones",
                                style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_traducir_tab()
        self.create_evaluar_tab()
        self.create_agregar_tab()
        self.create_estadisticas_tab()
        self.create_mejores_tab()
        self.create_peores_tab()
        self.create_guardar_cargar_tab()
        self.create_exportar_tab()
        self.create_historial_tab()
        
        self.status_bar = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_traducir_tab(self):
        """Crear pestaña de traducción"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['translate']} Traducir")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Traducir Texto", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        lang_frame = ttk.LabelFrame(main_frame, text="Selección de Idiomas", padding=10)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        origen_frame = ttk.Frame(lang_frame)
        origen_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(origen_frame, text="Idioma Origen:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.origen_var = tk.StringVar(value="español")
        origen_combo = ttk.Combobox(origen_frame, textvariable=self.origen_var, 
                                values=[idioma.value for idioma in Idioma], 
                                state="readonly", width=15)
        origen_combo.pack(side=tk.LEFT)
        
        destino_frame = ttk.Frame(lang_frame)
        destino_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(destino_frame, text="Idioma Destino:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.destino_var = tk.StringVar(value="inglés")
        destino_combo = ttk.Combobox(destino_frame, textvariable=self.destino_var,
                                    values=[idioma.value for idioma in Idioma],
                                    state="readonly", width=15)
        destino_combo.pack(side=tk.LEFT)
        
        text_frame = ttk.LabelFrame(main_frame, text="Texto a Traducir", padding=10)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.texto_entrada = scrolledtext.ScrolledText(text_frame, height=4, font=('Arial', 10))
        self.texto_entrada.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(button_frame, text="Traducir", command=self.traducir_texto,
                style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_traducir).pack(side=tk.LEFT)
        
        result_frame = ttk.LabelFrame(main_frame, text="Resultado", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.resultado_text = scrolledtext.ScrolledText(result_frame, height=6, font=('Arial', 10))
        self.resultado_text.pack(fill=tk.BOTH, expand=True)
    
    def traducir_texto(self):
        """Traducir el texto ingresado"""
        texto = self.texto_entrada.get("1.0", tk.END).strip()
        
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un texto para traducir.")
            return
        
        origen_str = self.origen_var.get()
        destino_str = self.destino_var.get()
        
        origen = self.string_to_idioma(origen_str)
        destino = self.string_to_idioma(destino_str)
        
        if origen == destino:
            messagebox.showwarning("Advertencia", "Los idiomas origen y destino deben ser diferentes.")
            return
        
        traduccion = self.traductor.traducir(origen, destino, texto)
        
        self.resultado_text.delete("1.0", tk.END)
        
        if traduccion:
            self.resultado_text.insert("1.0", f"✓ Traducción encontrada:\n\n")
            self.resultado_text.insert(tk.END, f"Texto original: {texto}\n")
            self.resultado_text.insert(tk.END, f"Traducción: {traduccion}\n\n")
            
            if self.traductor.existe_traduccion(origen, destino, texto):
                trad_obj = self.traductor.diccionario[origen][destino][texto.lower()]
                self.resultado_text.insert(tk.END, f"Confianza: {trad_obj.puntuacion_promedio:.1f}/10\n")
                self.resultado_text.insert(tk.END, f"Evaluaciones: {trad_obj.total_evaluaciones}")
            
            self.show_evaluation_frame(tab=self.notebook.nametowidget(self.notebook.select()), 
                                    origen=origen, destino=destino, texto=texto, traduccion=traduccion)
            
        else:
            self.resultado_text.insert("1.0", f"✗ No se encontró traducción para: {texto}\n\n")
            self.resultado_text.insert(tk.END, "¿Desea agregar esta traducción al diccionario?")
            
            self.show_add_confirmation_frame(tab=self.notebook.nametowidget(self.notebook.select()), 
                                        origen=origen, destino=destino, texto=texto)
        
        self.update_status("Traducción completada")
    
    def show_add_confirmation_frame(self, tab, origen, destino, texto):
        """Muestra un frame con botones para confirmar si se desea agregar la traducción"""
        for widget in tab.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and widget.winfo_name().startswith('confirm_frame'):
                widget.destroy()
        
        confirm_frame = ttk.LabelFrame(tab, text="Confirmar", padding=10)
        confirm_frame.pack(fill=tk.X, pady=(10, 0), after=self.resultado_text.master)
        
        ttk.Label(confirm_frame, text="¿Desea agregar esta traducción al diccionario?").pack(pady=(0, 10))
        
        button_frame = ttk.Frame(confirm_frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Agregar", 
                command=lambda: self.abrir_dialogo_agregar(origen, destino, texto, confirm_frame),
                style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Cancelar", 
                command=confirm_frame.destroy).pack(side=tk.LEFT)
    
    def abrir_dialogo_agregar(self, origen, destino, texto, confirm_frame):
        """Abre el diálogo para agregar traducción y luego destruye el frame de confirmación"""
        confirm_frame.destroy()
        self.show_add_translation_dialog(origen, destino, texto)
    
    def show_evaluation_frame(self, tab, origen, destino, texto, traduccion):
        """Mostrar frame para evaluar traducción existente"""
        for widget in tab.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and widget.winfo_name().startswith('eval_frame'):
                widget.destroy()
        
        eval_frame = ttk.LabelFrame(tab, text="Evaluar Traducción", padding=10)
        eval_frame.pack(fill=tk.X, pady=(10, 0), after=self.resultado_text.master)
        
        info_label = ttk.Label(eval_frame, 
                            text=f"¿Cómo calificaría esta traducción?", 
                            font=('Arial', 10))
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        scale_frame = ttk.Frame(eval_frame)
        scale_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(scale_frame, text="Puntuación (1-10):").pack(side=tk.LEFT, padx=(0, 10))
        
        puntuacion_var = tk.IntVar(value=5)
        scale = ttk.Scale(scale_frame, from_=1, to=10, variable=puntuacion_var,
                        orient=tk.HORIZONTAL, length=200)
        scale.pack(side=tk.LEFT)
        
        puntuacion_label = ttk.Label(scale_frame, text="5")
        puntuacion_label.pack(side=tk.LEFT, padx=(10, 0))
        
        def update_label(*args):
            puntuacion_label.config(text=str(puntuacion_var.get()))
        
        puntuacion_var.trace('w', update_label)
        
        button_frame = ttk.Frame(eval_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Enviar Evaluación", 
                command=lambda: self.evaluar_traduccion_gui(origen, destino, texto, puntuacion_var.get(), eval_frame),
                style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Omitir", 
                command=eval_frame.destroy).pack(side=tk.LEFT)
    
    def show_add_translation_dialog(self, origen, destino, texto):
        """Muestra un diálogo emergente para agregar una nueva traducción (sin selector de puntuación)"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nueva Traducción")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Agregar traducción para:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(main_frame, text=f"Texto original ({origen.value}): {texto}").pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text=f"Traducción en {destino.value}:").pack(anchor=tk.W)
        
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 10))
        
        nueva_traduccion_text = tk.Text(entry_frame, height=1, wrap="none", font=('Arial', 10))
        nueva_traduccion_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        h_scroll = ttk.Scrollbar(entry_frame, orient=tk.HORIZONTAL, command=nueva_traduccion_text.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        nueva_traduccion_text.configure(xscrollcommand=h_scroll.set)
        
        inversa_var = tk.BooleanVar(value=True)
        inversa_check = ttk.Checkbutton(main_frame, text="Agregar también traducción inversa",
                                    variable=inversa_var)
        inversa_check.pack(anchor=tk.W, pady=(0, 10))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        def agregar():
            nueva_traduccion = nueva_traduccion_text.get("1.0", "end-1c").strip()
            if not nueva_traduccion:
                messagebox.showwarning("Advertencia", "Por favor, ingrese una traducción.")
                return
            
            self.traductor.agregar_traduccion(origen, destino, texto, nueva_traduccion)
            
            if inversa_var.get():
                self.traductor.agregar_traduccion(destino, origen, nueva_traduccion, texto)
                messagebox.showinfo("Traducción Agregada", 
                                f"Traducción agregada: \"{texto}\" → \"{nueva_traduccion}\"\n\n" +
                                "Traducción inversa también agregada.")
            else:
                messagebox.showinfo("Traducción Agregada", 
                                f"Traducción agregada: \"{texto}\" → \"{nueva_traduccion}\"")
            
            dialog.destroy()
            self.limpiar_traducir()
        
        ttk.Button(button_frame, text="Agregar", command=agregar,
                style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT)
    
    def limpiar_traducir(self):
        """Limpiar campos de la pestaña de traducción"""
        self.texto_entrada.delete("1.0", tk.END)
        self.resultado_text.delete("1.0", tk.END)
        
        tab = self.notebook.nametowidget(self.notebook.select())
        for widget in tab.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                if widget.winfo_name().startswith(('eval_frame', 'confirm_frame')):
                    widget.destroy()
        
        self.update_status("Campos limpiados")
    
    def create_evaluar_tab(self):
        """Crear pestaña de evaluación"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['evaluate']} Evaluar")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Evaluar Traducción Existente", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        select_frame = ttk.LabelFrame(main_frame, text="Seleccionar Traducción", padding=10)
        select_frame.pack(fill=tk.X, pady=(0, 20))
        
        origen_frame = ttk.Frame(select_frame)
        origen_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(origen_frame, text="Idioma Origen:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.eval_origen_var = tk.StringVar(value="español")
        origen_combo = ttk.Combobox(origen_frame, textvariable=self.eval_origen_var,
                                values=[idioma.value for idioma in Idioma],
                                state="readonly", width=15)
        origen_combo.pack(side=tk.LEFT)
        
        destino_frame = ttk.Frame(select_frame)
        destino_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(destino_frame, text="Idioma Destino:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.eval_destino_var = tk.StringVar(value="inglés")
        destino_combo = ttk.Combobox(destino_frame, textvariable=self.eval_destino_var,
                                    values=[idioma.value for idioma in Idioma],
                                    state="readonly", width=15)
        destino_combo.pack(side=tk.LEFT)
        
        texto_frame = ttk.Frame(select_frame)
        texto_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(texto_frame, text="Texto Original:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.eval_texto_var = tk.StringVar()
        texto_entry = ttk.Entry(texto_frame, textvariable=self.eval_texto_var, width=40)
        texto_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(select_frame, text="Buscar Traducción", 
                command=self.buscar_traduccion_evaluar,
                style='Primary.TButton').pack(pady=(10, 0))
        
        self.eval_result_frame = ttk.LabelFrame(main_frame, text="Información de Traducción", padding=10)
        self.eval_result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.eval_result_text = scrolledtext.ScrolledText(self.eval_result_frame, height=8, font=('Arial', 10))
        self.eval_result_text.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_evaluar).pack(side=tk.LEFT)
    
    def buscar_traduccion_evaluar(self):
        """Buscar traducción para evaluar"""
        texto = self.eval_texto_var.get().strip()
        
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un texto.")
            return
        
        origen_str = self.eval_origen_var.get()
        destino_str = self.eval_destino_var.get()
        
        origen = self.string_to_idioma(origen_str)
        destino = self.string_to_idioma(destino_str)
        
        if origen == destino:
            messagebox.showwarning("Advertencia", "Los idiomas deben ser diferentes.")
            return
        
        if not self.traductor.existe_traduccion(origen, destino, texto):
            self.eval_result_text.delete("1.0", tk.END)
            self.eval_result_text.insert("1.0", f"✗ No existe traducción para: {texto}\n\n")
            self.eval_result_text.insert(tk.END, "Use la pestaña 'Traducir' para agregar una nueva traducción.")
            return
        
        traduccion = self.traductor.traducir(origen, destino, texto)
        trad_obj = self.traductor.diccionario[origen][destino][texto.lower()]
        
        self.eval_result_text.delete("1.0", tk.END)
        self.eval_result_text.insert("1.0", f"✓ Traducción encontrada:\n\n")
        self.eval_result_text.insert(tk.END, f"Texto original: {texto}\n")
        self.eval_result_text.insert(tk.END, f"Traducción: {traduccion}\n\n")
        self.eval_result_text.insert(tk.END, f"Puntuación actual: {trad_obj.puntuacion_promedio:.1f}/10\n")
        self.eval_result_text.insert(tk.END, f"Total evaluaciones: {trad_obj.total_evaluaciones}")
        
        self.show_eval_rating_frame(origen, destino, texto)
        
        self.update_status("Traducción encontrada")
    
    def show_eval_rating_frame(self, origen, destino, texto):
        """Mostrar frame para calificar traducción"""
        for widget in self.eval_result_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                widget.destroy()
        
        eval_rating_frame = ttk.LabelFrame(self.eval_result_frame, text="Evaluación", padding=10)
        eval_rating_frame.pack(fill=tk.X, pady=(10, 0))
        
        scale_frame = ttk.Frame(eval_rating_frame)
        scale_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(scale_frame, text="Nueva puntuación (1-10):").pack(side=tk.LEFT, padx=(0, 10))
        
        eval_puntuacion_var = tk.IntVar(value=5)
        scale = ttk.Scale(scale_frame, from_=1, to=10, variable=eval_puntuacion_var,
                        orient=tk.HORIZONTAL, length=200)
        scale.pack(side=tk.LEFT)
        
        eval_puntuacion_label = ttk.Label(scale_frame, text="5")
        eval_puntuacion_label.pack(side=tk.LEFT, padx=(10, 0))
        
        def update_label(*args):
            eval_puntuacion_label.config(text=str(eval_puntuacion_var.get()))
        
        eval_puntuacion_var.trace('w', update_label)
        
        ttk.Button(eval_rating_frame, text="Enviar Evaluación",
                command=lambda: self.enviar_evaluacion_gui(origen, destino, texto, eval_puntuacion_var.get(), eval_rating_frame),
                style='Success.TButton').pack()
    
    def limpiar_evaluar(self):
        """Limpiar la pestaña de evaluación por completo"""
        self.eval_texto_var.set("")
        self.eval_result_text.delete("1.0", tk.END)
        for widget in self.eval_result_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                widget.destroy()
        self.update_status("Campos limpiados")
    
    def create_agregar_tab(self):
        """Crear pestaña para agregar traducciones (sin selector de puntuación)"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['add']} Agregar")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Agregar Nueva Traducción", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        data_frame = ttk.LabelFrame(main_frame, text="Datos de Traducción", padding=15)
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        origen_frame = ttk.Frame(data_frame)
        origen_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(origen_frame, text="Idioma Origen:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.add_origen_var = tk.StringVar(value="español")
        origen_combo = ttk.Combobox(origen_frame, textvariable=self.add_origen_var,
                                values=[idioma.value for idioma in Idioma],
                                state="readonly", width=15)
        origen_combo.pack(side=tk.LEFT)
        
        destino_frame = ttk.Frame(data_frame)
        destino_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(destino_frame, text="Idioma Destino:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.add_destino_var = tk.StringVar(value="inglés")
        destino_combo = ttk.Combobox(destino_frame, textvariable=self.add_destino_var,
                                    values=[idioma.value for idioma in Idioma],
                                    state="readonly", width=15)
        destino_combo.pack(side=tk.LEFT)
        
        texto_frame = ttk.Frame(data_frame)
        texto_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(texto_frame, text="Texto Original:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.add_texto_var = tk.StringVar()
        texto_entry = ttk.Entry(texto_frame, textvariable=self.add_texto_var, width=40)
        texto_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        trad_frame = ttk.Frame(data_frame)
        trad_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(trad_frame, text="Traducción:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.add_traduccion_var = tk.StringVar()
        trad_entry = ttk.Entry(trad_frame, textvariable=self.add_traduccion_var, width=40)
        trad_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.add_inversa_var = tk.BooleanVar(value=True)
        inversa_check = ttk.Checkbutton(data_frame, text="Agregar también traducción inversa",
                                    variable=self.add_inversa_var)
        inversa_check.pack(anchor=tk.W, pady=(10, 0))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Agregar Traducción", 
                command=self.agregar_traduccion_manual,
                style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_agregar).pack(side=tk.LEFT)
    
    def create_estadisticas_tab(self):
        """Crear pestaña de estadísticas"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['stats']} Estadísticas")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Estadísticas del Traductor", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        ttk.Button(main_frame, text="Actualizar Estadísticas", 
                command=self.actualizar_estadisticas,
                style='Primary.TButton').pack(pady=(0, 20))
        
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas", padding=15)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=20, font=('Arial', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
    
    def actualizar_estadisticas(self):
        """Actualizar y mostrar estadísticas"""
        estadisticas = self.traductor.obtener_estadisticas()
        
        self.stats_text.delete("1.0", tk.END)
        
        self.stats_text.insert("1.0", "📊 ESTADÍSTICAS GENERALES\n")
        self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
        self.stats_text.insert(tk.END, f"• Total de traducciones: {estadisticas['total_traducciones']}\n")
        self.stats_text.insert(tk.END, f"• Total de evaluaciones: {estadisticas['total_evaluaciones']}\n")
        self.stats_text.insert(tk.END, f"• Puntuación global promedio: {estadisticas['puntuacion_global']:.2f}/10\n")
        self.stats_text.insert(tk.END, f"• Acciones en historial: {estadisticas['historial_traducciones']}\n\n")
        
        self.stats_text.insert(tk.END, "🌐 ESTADÍSTICAS POR IDIOMA\n")
        self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for idioma_str, stats in estadisticas['estadisticas_idiomas'].items():
            self.stats_text.insert(tk.END, f"\n{idioma_str.upper()}:\n")
            self.stats_text.insert(tk.END, f"  • Como origen: {stats['como_origen']} traducciones\n")
            self.stats_text.insert(tk.END, f"  • Como destino: {stats['como_destino']} traducciones\n")
            
            if stats['mejor_puntuacion'] > 0:
                self.stats_text.insert(tk.END, f"  • Mejor puntuación: {stats['mejor_puntuacion']:.1f}/10\n")
                self.stats_text.insert(tk.END, f"  • Peor puntuación: {stats['peor_puntuacion']:.1f}/10\n")
        
        self.update_status("Estadísticas actualizadas")
    
    def create_mejores_tab(self):
        """Crear pestaña de mejores traducciones"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['best']} Mejores")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Mejores Traducciones", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(control_frame, text="Idioma Origen:").pack(side=tk.LEFT, padx=(0, 10))
        self.best_origen_var = tk.StringVar(value="español")
        origen_combo = ttk.Combobox(control_frame, textvariable=self.best_origen_var,
                                values=[idioma.value for idioma in Idioma],
                                state="readonly", width=15)
        origen_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(control_frame, text="Idioma Destino:").pack(side=tk.LEFT, padx=(0, 10))
        self.best_destino_var = tk.StringVar(value="inglés")
        destino_combo = ttk.Combobox(control_frame, textvariable=self.best_destino_var,
                                    values=[idioma.value for idioma in Idioma],
                                    state="readonly", width=15)
        destino_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(control_frame, text="Mostrar:").pack(side=tk.LEFT, padx=(0, 10))
        self.best_limit_var = tk.StringVar(value="10")
        limit_spin = ttk.Spinbox(control_frame, from_=1, to=50, textvariable=self.best_limit_var,
                                width=5)
        limit_spin.pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="Buscar Mejores", 
                command=self.buscar_mejores,
                style='Primary.TButton').pack(side=tk.LEFT, padx=(20, 0))
        
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('#', 'Texto Original', 'Traducción', 'Puntuación', 'Evaluaciones')
        self.best_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.best_tree.heading(col, text=col)
            self.best_tree.column(col, width=100, anchor='center')
        
        self.best_tree.column('#', width=50, anchor='center')
        self.best_tree.column('Texto Original', width=200, anchor='w')
        self.best_tree.column('Traducción', width=200, anchor='w')
        self.best_tree.column('Puntuación', width=100, anchor='center')
        self.best_tree.column('Evaluaciones', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.best_tree.yview)
        self.best_tree.configure(yscrollcommand=scrollbar.set)
        
        self.best_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def buscar_mejores(self):
        """Buscar las mejores traducciones"""
        origen_str = self.best_origen_var.get()
        destino_str = self.best_destino_var.get()
        
        origen = self.string_to_idioma(origen_str)
        destino = self.string_to_idioma(destino_str)
        
        try:
            limite = int(self.best_limit_var.get())
        except ValueError:
            limite = 10
        
        mejores = self.traductor.obtener_mejores_traducciones(origen, destino, limite)
        
        for item in self.best_tree.get_children():
            self.best_tree.delete(item)
        
        for i, (texto_origen, traduccion) in enumerate(mejores, 1):
            self.best_tree.insert('', tk.END, values=(
                i,
                texto_origen,
                traduccion.texto,
                f"{traduccion.puntuacion_promedio:.1f}/10",
                traduccion.total_evaluaciones
            ))
        
        self.update_status(f"Mostrando {len(mejores)} mejores traducciones")
    
    def create_peores_tab(self):
        """Crear pestaña de peores traducciones"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['worst']} Peores")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Traducciones que Necesitan Mejora", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(control_frame, text="Idioma Origen:").pack(side=tk.LEFT, padx=(0, 10))
        self.worst_origen_var = tk.StringVar(value="español")
        origen_combo = ttk.Combobox(control_frame, textvariable=self.worst_origen_var,
                                values=[idioma.value for idioma in Idioma],
                                state="readonly", width=15)
        origen_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(control_frame, text="Idioma Destino:").pack(side=tk.LEFT, padx=(0, 10))
        self.worst_destino_var = tk.StringVar(value="inglés")
        destino_combo = ttk.Combobox(control_frame, textvariable=self.worst_destino_var,
                                    values=[idioma.value for idioma in Idioma],
                                    state="readonly", width=15)
        destino_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(control_frame, text="Mostrar:").pack(side=tk.LEFT, padx=(0, 10))
        self.worst_limit_var = tk.StringVar(value="10")
        limit_spin = ttk.Spinbox(control_frame, from_=1, to=50, textvariable=self.worst_limit_var,
                                width=5)
        limit_spin.pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="Buscar Peores", 
                command=self.buscar_peores,
                style='Warning.TButton').pack(side=tk.LEFT, padx=(20, 0))
        
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('#', 'Texto Original', 'Traducción', 'Puntuación', 'Evaluaciones')
        self.worst_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.worst_tree.heading(col, text=col)
            self.worst_tree.column(col, width=100, anchor='center')
        
        self.worst_tree.column('#', width=50, anchor='center')
        self.worst_tree.column('Texto Original', width=200, anchor='w')
        self.worst_tree.column('Traducción', width=200, anchor='w')
        self.worst_tree.column('Puntuación', width=100, anchor='center')
        self.worst_tree.column('Evaluaciones', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.worst_tree.yview)
        self.worst_tree.configure(yscrollcommand=scrollbar.set)
        
        self.worst_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def buscar_peores(self):
        """Buscar las peores traducciones"""
        origen_str = self.worst_origen_var.get()
        destino_str = self.worst_destino_var.get()
        
        origen = self.string_to_idioma(origen_str)
        destino = self.string_to_idioma(destino_str)
        
        try:
            limite = int(self.worst_limit_var.get())
        except ValueError:
            limite = 10
        
        peores = self.traductor.obtener_peores_traducciones(origen, destino, limite)
        
        for item in self.worst_tree.get_children():
            self.worst_tree.delete(item)
        
        for i, (texto_origen, traduccion) in enumerate(peores, 1):
            self.worst_tree.insert('', tk.END, values=(
                i,
                texto_origen,
                traduccion.texto,
                f"{traduccion.puntuacion_promedio:.1f}/10",
                traduccion.total_evaluaciones
            ))
        
        self.update_status(f"Mostrando {len(peores)} traducciones que necesitan mejora")
    
    def create_guardar_cargar_tab(self):
        """Crear pestaña para guardar y cargar diccionarios"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['load']} Guardar/Cargar")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Guardar, Cargar y Fusionar Diccionarios", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        save_frame = ttk.LabelFrame(main_frame, text="Guardar Diccionario", padding=15)
        save_frame.pack(fill=tk.X, pady=(0, 20))
        
        format_frame = ttk.Frame(save_frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(format_frame, text="Formato:").pack(side=tk.LEFT, padx=(0, 10))
        self.save_format_var = tk.StringVar(value="binario")
        ttk.Radiobutton(format_frame, text="Binario (.bin)", variable=self.save_format_var,
                    value="binario").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(format_frame, text="JSON (.json)", variable=self.save_format_var,
                    value="json").pack(side=tk.LEFT)
        
        file_frame = ttk.Frame(save_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text="Archivo:").pack(side=tk.LEFT, padx=(0, 10))
        self.save_file_var = tk.StringVar(value="diccionario_fusionado.bin")
        file_entry = ttk.Entry(file_frame, textvariable=self.save_file_var, width=40)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(file_frame, text="Examinar...", 
                command=self.examinar_guardar).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(save_frame, text="Guardar Diccionario", 
                command=self.guardar_diccionario_gui,
                style='Success.TButton').pack()
        
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        load_frame = ttk.LabelFrame(main_frame, text="Cargar Diccionario", padding=15)
        load_frame.pack(fill=tk.X)
        
        load_file_frame = ttk.Frame(load_frame)
        load_file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(load_file_frame, text="Archivo:").pack(side=tk.LEFT, padx=(0, 10))
        self.load_file_var = tk.StringVar()
        load_file_entry = ttk.Entry(load_file_frame, textvariable=self.load_file_var, width=40)
        load_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(load_file_frame, text="Examinar...", 
                command=self.examinar_cargar).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(load_frame, text="Cargar y Fusionar Diccionario", 
                command=self.cargar_diccionario_gui,
                style='Merge.TButton').pack()
        
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Checkbutton(options_frame, text="Activar modo fusión (recomendado)", 
                    variable=self.modo_fusion, 
                    command=self.actualizar_modo_fusion).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Button(options_frame, text="Limpiar Diccionario", 
                command=self.limpiar_diccionario_gui,
                style='Warning.TButton').pack(side=tk.LEFT)
    
    def actualizar_modo_fusion(self):
        """Actualizar el modo de fusión en la barra de estado"""
        if self.modo_fusion.get():
            self.status_bar.config(text="Listo - Modo: Fusión de diccionarios activado")
        else:
            self.status_bar.config(text="Listo - Modo: Reemplazo de diccionarios activado")
    
    def limpiar_diccionario_gui(self):
        """Limpia completamente el diccionario"""
        respuesta = messagebox.askyesno(
            "Confirmar", 
            "¿Está seguro de que desea limpiar completamente el diccionario?\n\n"
            "Esta acción eliminará todas las traducciones y el historial.\n"
            "No se puede deshacer."
        )
        
        if respuesta:
            exito, mensaje = self.traductor.limpiar_diccionario()
            if exito:
                messagebox.showinfo("Diccionario Limpiado", mensaje)
                self.update_status("Diccionario limpiado")
            else:
                messagebox.showerror("Error", mensaje)
    
    def create_exportar_tab(self):
        """Crear pestaña para exportar traducciones"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['export']} Exportar")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Exportar Traducciones", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding=15)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_text = "Exporte todas las traducciones a un archivo de texto legible.\n" \
                "El archivo contendrá todas las traducciones organizadas por idiomas."
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack()
        
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(file_frame, text="Archivo:").pack(side=tk.LEFT, padx=(0, 10))
        self.export_file_var = tk.StringVar(value="traducciones.txt")
        file_entry = ttk.Entry(file_frame, textvariable=self.export_file_var, width=40)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(file_frame, text="Examinar...", 
                command=self.examinar_exportar).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(main_frame, text="Exportar Traducciones", 
                command=self.exportar_traducciones_gui,
                style='Success.TButton').pack()
    
    def create_historial_tab(self):
        """Crear pestaña de historial"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"{self.icons['history']} Historial")
        
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="Historial de Acciones", 
                            style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        ttk.Button(main_frame, text="Actualizar Historial", 
                command=self.actualizar_historial,
                style='Primary.TButton').pack(pady=(0, 20))
        
        hist_frame = ttk.LabelFrame(main_frame, text="Últimas Acciones", padding=10)
        hist_frame.pack(fill=tk.BOTH, expand=True)
        
        self.hist_text = scrolledtext.ScrolledText(hist_frame, height=20, font=('Arial', 10))
        self.hist_text.pack(fill=tk.BOTH, expand=True)
    
    def actualizar_historial(self):
        """Actualizar y mostrar historial"""
        if not self.traductor.historial_traducciones:
            self.hist_text.delete("1.0", tk.END)
            self.hist_text.insert("1.0", "No hay historial registrado.")
            return
        
        historial_reciente = self.traductor.historial_traducciones[-50:]
        
        self.hist_text.delete("1.0", tk.END)
        self.hist_text.insert("1.0", f"Últimas {len(historial_reciente)} acciones:\n")
        self.hist_text.insert(tk.END, "=" * 60 + "\n\n")
        
        for i, registro in enumerate(reversed(historial_reciente), 1):
            fecha_str = registro['fecha'].strftime("%Y-%m-%d %H:%M:%S")
            accion = registro['accion']
            
            if accion == 'traducir':
                self.hist_text.insert(tk.END, f"{i:2}. [{fecha_str}] 📝 Traducir\n")
                self.hist_text.insert(tk.END, f"     {registro['origen'].value} → {registro['destino'].value}\n")
                self.hist_text.insert(tk.END, f"     \"{registro['texto_origen']}\" → \"{registro['texto_traduccion']}\"\n")
                if 'puntuacion' in registro:
                    self.hist_text.insert(tk.END, f"     Puntuación: {registro['puntuacion']:.1f}/10\n")
                self.hist_text.insert(tk.END, "\n")
            
            elif accion == 'evaluar':
                self.hist_text.insert(tk.END, f"{i:2}. [{fecha_str}] ⭐ Evaluar\n")
                self.hist_text.insert(tk.END, f"     {registro['origen'].value} → {registro['destino'].value}\n")
                self.hist_text.insert(tk.END, f"     \"{registro['texto_origen']}\"\n")
                self.hist_text.insert(tk.END, f"     Nueva puntuación: {registro['puntuacion']}/10\n")
                self.hist_text.insert(tk.END, f"     Anterior: {registro['puntuacion_anterior']:.1f}/10\n")
                self.hist_text.insert(tk.END, "\n")
            
            elif accion == 'agregar':
                self.hist_text.insert(tk.END, f"{i:2}. [{fecha_str}] ➕ Agregar\n")
                self.hist_text.insert(tk.END, f"     {registro['origen'].value} → {registro['destino'].value}\n")
                self.hist_text.insert(tk.END, f"     \"{registro['texto_origen']}\" → \"{registro['texto_traduccion']}\"\n")
                self.hist_text.insert(tk.END, "\n")
        
        self.hist_text.insert(tk.END, f"\nTotal en historial: {len(self.traductor.historial_traducciones)} acciones")
        self.update_status("Historial actualizado")
    
    def string_to_idioma(self, idioma_str):
        """Convertir string a enum Idioma"""
        for idioma in Idioma:
            if idioma.value == idioma_str:
                return idioma
        return Idioma.ESPANOL  
    
    def evaluar_traduccion_gui(self, origen, destino, texto, puntuacion, frame):
        """Evaluar traducción desde la GUI y limpiar la pestaña"""
        exito, mensaje = self.traductor.evaluar_traduccion(origen, destino, texto, puntuacion)
        
        if exito:
            messagebox.showinfo("Evaluación Registrada", mensaje)
            frame.destroy()
            self.limpiar_traducir()
        else:
            messagebox.showerror("Error", mensaje)
    
    def agregar_traduccion_manual(self):
        """Agregar traducción manual desde la pestaña correspondiente (sin puntuación)"""
        texto = self.add_texto_var.get().strip()
        traduccion = self.add_traduccion_var.get().strip()
        
        if not texto or not traduccion:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return
        
        origen_str = self.add_origen_var.get()
        destino_str = self.add_destino_var.get()
        
        origen = self.string_to_idioma(origen_str)
        destino = self.string_to_idioma(destino_str)
        
        if origen == destino:
            messagebox.showwarning("Advertencia", "Los idiomas deben ser diferentes.")
            return
        
        self.traductor.agregar_traduccion(origen, destino, texto, traduccion)
        
        if self.add_inversa_var.get():
            self.traductor.agregar_traduccion(destino, origen, traduccion, texto)
        
        messagebox.showinfo("Éxito", "Traducción agregada exitosamente.")
        self.limpiar_agregar()
    
    def enviar_evaluacion_gui(self, origen, destino, texto, puntuacion, frame):
        """Enviar evaluación desde la pestaña de evaluación"""
        exito, mensaje = self.traductor.evaluar_traduccion(origen, destino, texto, puntuacion)
        
        if exito:
            messagebox.showinfo("Evaluación Registrada", mensaje)
            frame.destroy()
            self.buscar_traduccion_evaluar() 
        else:
            messagebox.showerror("Error", mensaje)
    
    def limpiar_agregar(self):
        """Limpiar campos de la pestaña agregar"""
        self.add_texto_var.set("")
        self.add_traduccion_var.set("")
        self.update_status("Campos limpiados")
    
    def examinar_guardar(self):
        """Abrir diálogo para seleccionar archivo para guardar"""
        formato = self.save_format_var.get()
        extension = ".bin" if formato == "binario" else ".json"
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=[
                ("Archivo binario", "*.bin"),
                ("Archivo JSON", "*.json"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.save_file_var.set(archivo)
    
    def examinar_cargar(self):
        """Abrir diálogo para seleccionar archivo para cargar"""
        archivo = filedialog.askopenfilename(
            filetypes=[
                ("Archivo binario", "*.bin"),
                ("Archivo JSON", "*.json"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.load_file_var.set(archivo)
    
    def examinar_exportar(self):
        """Abrir diálogo para seleccionar archivo para exportar"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Archivo de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.export_file_var.set(archivo)
    
    def guardar_diccionario_gui(self):
        """Guardar diccionario desde la GUI"""
        archivo = self.save_file_var.get()
        formato = self.save_format_var.get()
        
        if not archivo:
            messagebox.showwarning("Advertencia", "Por favor, especifique un archivo.")
            return
        
        if formato == "binario":
            exito, mensaje = self.traductor.guardar_diccionario_binario(archivo)
        else:
            exito, mensaje = self.traductor.guardar_diccionario_json(archivo)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
    
    def cargar_diccionario_gui(self):
        """Cargar diccionario desde la GUI"""
        archivo = self.load_file_var.get()
        
        if not archivo:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo.")
            return
        
        fusionar = self.modo_fusion.get()
        
        if archivo.endswith('.json'):
            exito, mensaje = self.traductor.cargar_diccionario_json(archivo, fusionar)
        else:
            exito, mensaje = self.traductor.cargar_diccionario_binario(archivo, fusionar)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_estadisticas()
        else:
            messagebox.showerror("Error", mensaje)
    
    def exportar_traducciones_gui(self):
        """Exportar traducciones desde la GUI"""
        archivo = self.export_file_var.get()
        
        if not archivo:
            messagebox.showwarning("Advertencia", "Por favor, especifique un archivo.")
            return
        
        exito, mensaje = self.traductor.exportar_traducciones_texto(archivo)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
    
    def update_status(self, message):
        """Actualizar mensaje en la barra de estado"""
        modo = "Fusión" if self.modo_fusion.get() else "Reemplazo"
        total_traducciones = self.traductor.obtener_total_traducciones()
        self.status_bar.config(text=f"Estado: {message} | Modo: {modo} | Traducciones: {total_traducciones}")
        self.root.after(5000, lambda: self.actualizar_barra_estado())
    
    def actualizar_barra_estado(self):
        """Actualizar la barra de estado con el modo actual"""
        modo = "Fusión" if self.modo_fusion.get() else "Reemplazo"
        total_traducciones = self.traductor.obtener_total_traducciones()
        self.status_bar.config(text=f"Listo | Modo: {modo} | Traducciones: {total_traducciones}")

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = TraductorAprendizajeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
