import re
from datetime import datetime

def validar_email(email):
    """
    Valida formato de email según el patrón: texto@texto.dominio
    
    Args:
        email (str): Email a validar
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not email:
        return False, "El email es obligatorio"
    
    # Patrón regex para validar email
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Formato de email inválido. Use: texto@texto.dominio"
    
    if len(email) > 100:
        return False, "Email muy largo (máximo 100 caracteres)"
    
    return True, None


def validar_celular(celular):
    """
    Valida formato de celular (OPCIONAL)
    Formato esperado: +569.12345678
    
    Args:
        celular (str): Número de celular a validar
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not celular:
        return True, None  # Es opcional, si está vacío es válido
    
    # Patrón: +569.12345678 (código país + punto + 8 dígitos)
    pattern = r'^\+[0-9]{3}\.[0-9]{8}$'
    
    if not re.match(pattern, celular):
        return False, "Formato de celular inválido. Use: +569.12345678"
    
    return True, None


def validar_nombre(nombre):
    """
    Valida nombre del contacto
    Debe tener entre 3 y 200 caracteres
    
    Args:
        nombre (str): Nombre a validar
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not nombre:
        return False, "El nombre es obligatorio"
    
    if len(nombre) < 3:
        return False, "El nombre debe tener al menos 3 caracteres"
    
    if len(nombre) > 200:
        return False, "El nombre es muy largo (máximo 200 caracteres)"
    
    return True, None


def validar_fecha_entrega(fecha_str):
    """
    Valida que la fecha de entrega sea válida y futura
    
    Args:
        fecha_str (str): Fecha en formato ISO (YYYY-MM-DDTHH:MM)
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not fecha_str:
        return False, "La fecha de entrega es obligatoria"
    
    try:
        # Intentar parsear la fecha
        # Soportar tanto formato con Z como sin Z
        fecha_str_limpia = fecha_str.replace('Z', '')
        fecha = datetime.fromisoformat(fecha_str_limpia)
        
        # Verificar que sea futura (al menos 1 hora adelante)
        ahora = datetime.now()
        
        if fecha <= ahora:
            return False, "La fecha de entrega debe ser futura"
        
        # Verificar que no sea muy lejana (opcional, por ejemplo máximo 1 año)
        diferencia_dias = (fecha - ahora).days
        if diferencia_dias > 365:
            return False, "La fecha de entrega no puede ser más de 1 año en el futuro"
        
        return True, None
        
    except ValueError as e:
        return False, f"Formato de fecha inválido: {str(e)}"
    except Exception as e:
        return False, "Error al validar la fecha"


def validar_archivo(file):
    """
    Valida que el archivo sea una imagen válida
    
    Args:
        file: Objeto FileStorage de Flask
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
    
    if not file:
        return False, "No se ha proporcionado un archivo"
    
    if not file.filename or file.filename == '':
        return False, "El archivo no tiene nombre"
    
    # Obtener extensión del archivo
    if '.' not in file.filename:
        return False, "El archivo no tiene extensión"
    
    ext = file.filename.rsplit('.', 1)[1].lower()
    
    if ext not in allowed_extensions:
        return False, f"Extensión no permitida. Use: {', '.join(allowed_extensions)}"
    
    return True, None


def sanitizar_texto(texto):
    """
    Sanitiza texto para prevenir XSS básico
    
    Args:
        texto (str): Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not texto:
        return texto
    
    # Reemplazar caracteres peligrosos
    texto = texto.replace('<', '&lt;')
    texto = texto.replace('>', '&gt;')
    texto = texto.replace('"', '&quot;')
    texto = texto.replace("'", '&#39;')
    
    return texto


def validar_entero_positivo(valor, nombre_campo, minimo=1, maximo=None):
    """
    Valida que un valor sea un entero positivo
    
    Args:
        valor: Valor a validar
        nombre_campo (str): Nombre del campo para el mensaje de error
        minimo (int): Valor mínimo permitido
        maximo (int): Valor máximo permitido (None = sin límite)
        
    Returns:
        tuple: (bool, str, int) - (es_válido, mensaje_error, valor_convertido)
    """
    if valor is None or valor == '':
        return False, f"{nombre_campo} es obligatorio", None
    
    try:
        valor_int = int(valor)
        
        if valor_int < minimo:
            return False, f"{nombre_campo} debe ser al menos {minimo}", None
        
        if maximo is not None and valor_int > maximo:
            return False, f"{nombre_campo} no puede ser mayor a {maximo}", None
        
        return True, None, valor_int
        
    except (ValueError, TypeError):
        return False, f"{nombre_campo} debe ser un número válido", None


def validar_enum(valor, opciones_validas, nombre_campo):
    """
    Valida que un valor esté dentro de opciones permitidas (ENUM)
    
    Args:
        valor: Valor a validar
        opciones_validas (list): Lista de opciones válidas
        nombre_campo (str): Nombre del campo para el mensaje de error
        
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not valor:
        return False, f"{nombre_campo} es obligatorio"
    
    if valor not in opciones_validas:
        return False, f"{nombre_campo} no es válido. Opciones: {', '.join(opciones_validas)}"
    
    return True, None
