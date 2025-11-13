# servicios.py

from modelos import Votante, Voto
import os  
import random
import smtplib  # Para enviar correos
import ssl      # Para la conexión segura
     # (Opcional, para seguridad)

# --- TU EMAIL Y CONTRASEÑA ---
# !! NO SUBAS ESTO A GITHUB CON TU CONTRASEÑA ESCRITA AQUÍ !!
# (Forma segura es usar variables de entorno)
# (Forma insegura pero rápida para probar:)
EMAIL_EMISOR = os.environ.get('GMAIL_EMAIL')
PASSWORD_EMISOR = os.environ.get('GMAIL_PASSWORD')  # La contraseña de 16 letras que generaste

class AuthService:
    # ... (Esta clase no cambia, la dejamos igual) ...
    def registrar_votante(self, correo, db_votantes_lista):
        if not correo.endswith("@uni.pe"):
            return None, "Error: El correo no es institucional (@uni.pe)."
        
        for votante in db_votantes_lista:
            if votante.correo_uni == correo:
                return None, "Error: Votante ya está registrado."
        
        nuevo_votante = Votante(correo_uni=correo)
        db_votantes_lista.append(nuevo_votante)
        
        return nuevo_votante, "Registro exitoso. Revisa tu correo por el código."


class EmailService:
    """
    ENVÍA UN CORREO REAL (Versión Plan C - Saltando verificación SSL)
    """
    def enviar_codigo_verificacion(self, votante_obj):
        codigo = str(random.randint(100000, 999999))
        votante_obj.codigo_verificacion = codigo
        
        # --- ¡¡CAMBIO IMPORTANTE AQUÍ!! ---
        # Le decimos a SSL que NO verifique los certificados.
        # Esto soluciona el error 'CERTIFICATE_VERIFY_FAILED' en algunas PC Windows.
        # Es menos seguro, pero bueno para desarrollo.
        contexto_ssl = ssl._create_unverified_context()
        # ------------------------------------

        servidor_smtp = "smtp.gmail.com"
        puerto = 587  # Puerto para STARTTLS

        asunto = "Tu Código de Votación Institucional"
        cuerpo_mensaje = f"Hola,\n\nTu código para votar es: {codigo}\n\nGracias."
        
        mensaje_completo = f"Subject: {asunto}\n\n{cuerpo_mensaje}".encode('utf-8')
        
        try:
            servidor = smtplib.SMTP(servidor_smtp, puerto)
            servidor.starttls(context=contexto_ssl) # Usamos el contexto no verificado
            servidor.login(EMAIL_EMISOR, PASSWORD_EMISOR)
            
            print(f"Enviando correo real (vía STARTTLS) a: {votante_obj.correo_uni}")
            servidor.sendmail(EMAIL_EMISOR, votante_obj.correo_uni, mensaje_completo)
            
            servidor.quit()
            print("Correo enviado exitosamente.")
            return True
            
        except Exception as e:
            # Imprimimos el error en la consola
            print(f"ERROR al enviar correo (STARTTLS): {e}") 
            return False

class VotacionService:
    # ... (Esta clase no cambia) ...
    def emitir_voto(self, codigo_ingresado, candidato_id_seleccionado, db_votantes, db_votos):
        votante_encontrado = None
        for votante in db_votantes:
            if votante.codigo_verificacion == codigo_ingresado:
                votante_encontrado = votante
                break 
        
        if not votante_encontrado:
            return False, "Error: El código de verificación es incorrecto."
            
        if votante_encontrado.ha_votado:
            return False, "Error: Este código ya fue utilizado para votar."
            
        votante_encontrado.ha_votado = True
        
        nuevo_voto = Voto(
            votante_correo=votante_encontrado.correo_uni,
            candidato_id=candidato_id_seleccionado
        )
        db_votos.append(nuevo_voto) 
        
        return True, "¡Voto registrado! Gracias por participar."