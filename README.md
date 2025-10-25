# Tarea 3: Sistema de Gestión de Avisos de Adopción de Mascotas

## 👤 Autor

**Jules Paz Fredes Cerain**  
CC5002 - Desarrollo de Aplicaciones Web

---

## Decisiones de Implementación

### 1. Sistema de Comentarios

**Validaciones:**

- **Nombre:** 3-80 caracteres (validado en cliente y servidor)
- **Comentario:** mínimo 5 caracteres (validado en cliente y servidor)

**Características:**

- Llamadas asíncronas con `fetch()` API (sin recargar página)
- Comentarios ordenados por fecha descendente (más recientes primero)
- Formato de fecha: `dd/mm/yyyy HH:MM`

### 2. Estadísticas con Chart.js

**Gráficos implementados:**

1. **Líneas:** Avisos de adopción por día
2. **Torta:** Distribución por tipo de mascota (Gatos vs Perros)
3. **Barras:** Avisos por mes y tipo de mascota

**Características:**

- Todas las estadísticas usan llamadas asíncronas a APIs REST
- Compatibilidad con SQLite y MySQL (agrupación por mes implementada en Python)
- Colores consistentes: `#d74967` (rosa), `#f47066` (coral), `#a7a6da` (lavanda)

### 3. Base de Datos

**Configuración:**

- Usuario: `cc5002`
- Contraseña: `programacionweb`
- Base de datos: `tarea2`

**Modelo Comentario:**

```python
id: Integer (PK)
nombre: String(80)
texto: Text
fecha: DateTime
aviso_id: Integer (FK -> aviso_adopcion.id)
```

---

## 🚀 Configuración y Ejecución

### 1. Configurar Base de Datos

```bash
# Ejecutar scripts SQL (requiere MySQL instalado)
mysql -u root -p < db/tarea2.sql
mysql -u cc5002 -p tarea2 < db/region-comuna.sql
```

### 2. Instalar Dependencias

```bash
# Crear entorno virtual (si no existe)
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Instalar paquetes requeridos
pip install flask flask-sqlalchemy pymysql cryptography
```

### 3. Ejecutar Aplicación

```bash
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
