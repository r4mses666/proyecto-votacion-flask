#Definamos las clases:

class Votante:
    """
    Representa a un estudiante habilitado para votar.
    """
    def __init__(self, correo_uni, nombre=""):
        # --- Atributos (Datos) ---
        self.correo_uni = correo_uni
        self.nombre = nombre
        self.codigo_verificacion = "" # El código único que se le enviará
        self.ha_votado = False        # Control para asegurar un solo voto

class Candidato:
    """
    Representa a una persona que se postula a un cargo.
    """
    def __init__(self, id_candidato, nombre, partido):
        # --- Atributos ---
        self.id_candidato = id_candidato
        self.nombre = nombre
        self.partido = partido

class Eleccion:
    """
    Representa el evento de votación en sí. Contiene a los candidatos.
    """
    def __init__(self, nombre):
        # --- Atributos ---
        self.nombre = nombre
        self.candidatos = [] # Es una lista de objetos de la clase Candidato

    # --- Métodos (Comportamientos) ---
    def agregar_candidato(self, candidato):
        """Añade un objeto Candidato a la lista de esta elección."""
        self.candidatos.append(candidato)

    def obtener_candidatos(self):
        """Devuelve la lista de candidatos."""
        return self.candidatos

class Voto:
    """
    Representa la acción de un voto emitido. 
    Es un registro de que un votante eligió a un candidato.
    """
    def __init__(self, votante_correo, candidato_id):
        # --- Atributos ---
        self.votante_correo = votante_correo
        self.candidato_id = candidato_id
        # En un sistema real, aquí guardarías la fecha y hora.