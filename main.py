# main.py
# Importamos las *clases* (plantillas) que necesitamos
from modelos import Eleccion, Candidato
from servicios import AuthService, EmailService, VotacionService

def iniciar_simulacion():
    
    # --- 1. CONFIGURACIÓN INICIAL (El "Setup") ---
    print("===== CONFIGURANDO SISTEMA DE VOTACIÓN =====")
    
    # Creamos las instancias (objetos) de nuestros servicios
    auth_service = AuthService()
    email_service = EmailService()
    votacion_service = VotacionService()
    
    # Creamos nuestras "Bases de Datos" (son listas vacías al inicio)
    # Estas listas guardarán los OBJETOS
    db_votantes_registrados = []
    db_votos_emitidos = []
    
    # Creamos la elección y los candidatos
    eleccion_actual = Eleccion(nombre="Elección del Consejo Estudiantil 2025")
    eleccion_actual.agregar_candidato(Candidato(id_candidato="C1", nombre="Ana Gómez", partido="Partido Innova"))
    eleccion_actual.agregar_candidato(Candidato(id_candidato="C2", nombre="Luis Torres", partido="Partido Progresa"))
    
    print(f"Elección '{eleccion_actual.nombre}' configurada con {len(eleccion_actual.candidatos)} candidatos.\n")

    
    # --- 2. FLUJO DE REGISTRO (Simulamos usuarios registrándose) ---
    print("===== FASE DE REGISTRO =====")
    
    # Usuario 1 se registra
    correo_1 = "juan.perez@mi-uni.edu"
    votante_1, msg_1 = auth_service.registrar_votante(correo_1, db_votantes_registrados)
    print(msg_1)
    
    # Usuario 2 se registra
    correo_2 = "maria.lopez@mi-uni.edu"
    votante_2, msg_2 = auth_service.registrar_votante(correo_2, db_votantes_registrados)
    print(msg_2)
    
    # Usuario 3 (inválido) intenta registrarse
    correo_3 = "intruso@gmail.com"
    votante_3, msg_3 = auth_service.registrar_votante(correo_3, db_votantes_registrados)
    print(msg_3)
    
    print("\nEnviando códigos de verificación...")
    codigo_votante_1 = ""
    if votante_1:
        email_service.enviar_codigo_verificacion(votante_1)
        codigo_votante_1 = votante_1.codigo_verificacion # Guardamos su código
        
    codigo_votante_2 = ""
    if votante_2:
        email_service.enviar_codigo_verificacion(votante_2)
        codigo_votante_2 = votante_2.codigo_verificacion # Guardamos su código


    # --- 3. FLUJO DE VOTACIÓN (Simulamos la votación) ---
    print("\n===== FASE DE VOTACIÓN =====")
    
    # Votante 1 (Juan) vota por el Candidato C1
    print(f"\n{correo_1} intenta votar...")
    exito, msg = votacion_service.emitir_voto(
        codigo_ingresado=codigo_votante_1, 
        candidato_id_seleccionado="C1", 
        db_votantes=db_votantes_registrados, 
        db_votos=db_votos_emitidos
    )
    print(msg)
    
    # Votante 2 (María) vota por el Candidato C2
    print(f"\n{correo_2} intenta votar...")
    exito, msg = votacion_service.emitir_voto(
        codigo_ingresado=codigo_votante_2, 
        candidato_id_seleccionado="C2", 
        db_votantes=db_votantes_registrados, 
        db_votos=db_votos_emitidos
    )
    print(msg)
    
    
    # --- 4. PRUEBAS DE SEGURIDAD (¿Qué pasa si intentan votar de nuevo?) ---
    print("\n===== PRUEBAS DE SEGURIDAD =====")
    
    # Votante 1 (Juan) intenta votar DE NUEVO
    print(f"\n{correo_1} intenta votar por segunda vez...")
    exito, msg = votacion_service.emitir_voto(
        codigo_ingresado=codigo_votante_1, 
        candidato_id_seleccionado="C2", 
        db_votantes=db_votantes_registrados, 
        db_votos=db_votos_emitidos
    )
    print(msg) # Debería fallar
    

    # --- 5. RESULTADOS (Simulación de ReporteService) ---
    print("\n===== CONTEO FINAL DE VOTOS =====")
    print(f"Total de votos emitidos válidamente: {len(db_votos_emitidos)}")
    
    conteo_final = {}
    for candidato in eleccion_actual.obtener_candidatos():
        conteo_final[candidato.nombre] = 0 # Inicializa el conteo en 0
        
    for voto in db_votos_emitidos:
        # Buscamos al candidato por su ID
        for candidato in eleccion_actual.obtener_candidatos():
            if voto.candidato_id == candidato.id_candidato:
                conteo_final[candidato.nombre] += 1
                
    print("Resultados:")
    print(conteo_final)

# --- Punto de entrada del programa ---
if __name__ == "__main__":
    iniciar_simulacion()