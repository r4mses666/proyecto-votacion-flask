# --- 1. IMPORTACIONES ---
import os
from flask import Flask, render_template, request, jsonify
from modelos import Eleccion, Candidato
# Asegúrate de que el 'servicios.py' que estés usando sea el del "Plan C"
# (el que usa ssl._create_unverified_context())
from servicios import AuthService, EmailService, VotacionService

# --- 2. DEFINICIÓN DE 'app' (NIVEL SUPERIOR) ---
app = Flask(__name__)

# --- 3. CONFIGURACIÓN Y VARIABLES GLOBALES ---
print(">>> Creando instancias de servicios...")
auth_service = AuthService()
email_service = EmailService()
votacion_service = VotacionService()

print(">>> Creando bases de datos en memoria...")
db_votantes_registrados = []
db_votos_emitidos = []

print(">>> Configurando la elección...")
eleccion_actual = Eleccion(nombre="Elección de Delegado Estudiantil FIEE")
eleccion_actual.agregar_candidato(Candidato(id_candidato="c_abdel", nombre="Abdel", partido="Partido Voltio"))
eleccion_actual.agregar_candidato(Candidato(id_candidato="c_angelo", nombre="Angelo", partido="Partido Circuito"))

print(">>> Archivo app.py leído por Python. Rutas listas.")


# --- 4. RUTAS (endpoints) ---

@app.route("/")
def pagina_principal():
    """
    Entrega la página web principal (index.html).
    """
    print("Acceso a la ruta principal (/)")
    return render_template(
        'index.html', 
        titulo_eleccion=eleccion_actual.nombre,
        lista_candidatos=eleccion_actual.obtener_candidatos()
    )

@app.route("/api/registrar", methods=['POST'])
def api_registrar_votante():
    """
    API para registrar un votante y enviarle un código.
    (Versión con el bug de respuesta corregido)
    """
    print("Recibida peticion en /api/registrar")
    datos = request.json
    correo = datos.get('correo')
    
    # 1. Intenta registrar al votante (validar @uni.pe, etc.)
    votante_obj, mensaje = auth_service.registrar_votante(correo, db_votantes_registrados)
    
    if votante_obj:
        # 2. Si el registro es válido, intenta enviar el email
        print(f"Registrando a {correo}...")
        exito_email = email_service.enviar_codigo_verificacion(votante_obj)
        
        # 3. Verificamos si el email se ENVIÓ
        if exito_email:
            # ¡SÍ SE ENVIÓ! Respondemos 200 (Éxito)
            print("Correo parece haber sido enviado.")
            return jsonify({'exito': True, 'mensaje': "Registro exitoso. ¡Revisa tu correo!"}), 200
        else:
            # ¡FALLÓ EL ENVÍO! Respondemos 500 (Error del Servidor)
            print("El envío de correo falló. Ver log.")
            return jsonify({'exito': False, 'mensaje': "El correo es válido, pero no pudimos enviar el código. Contacta al administrador."}), 500
            
    else:
        # 1b. Si el registro falló (ej: correo no es @uni.pe)
        print(f"Error de registro para {correo}: {mensaje}")
        return jsonify({'exito': False, 'mensaje': mensaje}), 400

@app.route("/api/votar", methods=['POST'])
def api_emitir_voto():
    """
    API para verificar el código y registrar un voto.
    """
    print("Recibida petición en /api/votar")
    datos = request.json
    codigo = datos.get('codigo')
    candidato_id = datos.get('candidato_id')
    
    exito, mensaje = votacion_service.emitir_voto(
        codigo_ingresado=codigo,
        candidato_id_seleccionado=candidato_id,
        db_votantes=db_votantes_registrados,
        db_votos=db_votos_emitidos
    )
    
    if exito:
        print(f"Voto exitoso con código {codigo} para {candidato_id}")
        return jsonify({'exito': True, 'mensaje': mensaje}), 200
    else:
        print(f"Voto fallido con código {codigo}: {mensaje}")
        return jsonify({'exito': False, 'mensaje': mensaje}), 400

@app.route("/api/resultados")
def api_resultados():
    """
    API para que el gráfico de Chart.js obtenga los datos.
    """
    print("Recibida petición en /api/resultados")
    conteo_final = {}
    
    for candidato in eleccion_actual.obtener_candidatos():
        conteo_final[candidato.nombre] = 0
    
    for voto in db_votos_emitidos:
        for candidato in eleccion_actual.obtener_candidatos():
            if voto.candidato_id == candidato.id_candidato:
                conteo_final[candidato.nombre] += 1
    
    labels = list(conteo_final.keys())
    data = list(conteo_final.values())
    
    print(f"Enviando resultados: {labels} - {data}")
    return jsonify({'labels': labels, 'data': data})
        

# --- 5. PUNTO DE ENTRADA (SOLO PARA PRUEBAS LOCALES) ---
if __name__ == "__main__":
    print("Iniciando servidor local de Flask...")
    app.run(debug=True, port=5000)