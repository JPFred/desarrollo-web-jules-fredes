# Tarea 2: Sistema de Gestión de Avisos de Adopción de Mascotas

## 👤 Autor

**Jules Paz Fredes Cerain**  
CC5002 - Desarrollo de Aplicaciones Web  

---

## 🛠️ Tecnologías Utilizadas

### Backend
| Tecnología |
|------------|
| **Python 3.11+** |
| **Flask 3.0.0** |
| **SQLAlchemy** |
| **MySQL 8.0+** |
| **PyMySQL** |

### Frontend
| Tecnología |
|------------|
| **HTML5** |
| **CSS3** |
| **JavaScript ES6** |
| **Jinja2** |

---

## 📋 Decisiones de Implementación

### Configuración de Base de Datos
- Usuario: `cc5002`
- Contraseña: `programacionweb`
- Base de datos: `tarea2`

### Formato de Celular
Implementado como `+NNN.NNNNNNNN` (ejemplo: `+569.12345678`). El campo es opcional.

### Validación de Fotos
- Mínimo 1 foto, máximo 5 fotos por aviso
- Formatos aceptados: png, jpg, jpeg, gif, webp, bmp
- Tamaño máximo: 5MB por foto
- Almacenadas en `static/uploads/` con nombres seguros

### Paginación
15 avisos por página en `/ver-listado` según especificación.

### Validaciones
Validaciones JavaScript del cliente se replican en el servidor para seguridad:
- Región/Comuna con verificación de relación
- Email formato `texto@texto.dominio`
- Nombre 3-200 caracteres
- Fecha de entrega futura
- Fotos: tipo, tamaño y cantidad

### Estadísticas
El botón aparece deshabilitado con mensaje "Funcionalidad pendiente para la Tarea 3".  
La ruta `/estadisticas` no está implementada.

### Seguridad
- SQLAlchemy ORM (prevención SQL Injection)
- Escape automático Jinja2 (prevención XSS)
- `secure_filename()` para archivos
- Validación de tipos MIME

---

## 🚀 Ejecución

```bash
# Configurar base de datos
mysql -u root -p < db/tarea2.sql
mysql -u cc5002 -p tarea2 < db/region-comuna.sql

# Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install flask flask-sqlalchemy pymysql python-dotenv werkzeug

# Ejecutar
python app.py
```

Acceso: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🎨 Diseño Visual

### Paleta de Colores

- **Principal**: `#d74967` (Rosa vibrante)
- **Secundario**: `#f47066` (Coral)
- **Acento**: `#a7a6da` (Lavanda)
- **Fondo**: `#e2e4f4` (Azul claro)
