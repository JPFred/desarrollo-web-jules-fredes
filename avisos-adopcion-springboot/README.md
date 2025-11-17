# Sistema de Avisos de Adopción - Tarea 4

## Autor
**Jules Paz Fredes Cerain**  
CC5002 - Desarrollo de Aplicaciones Web  
Universidad de Chile

## Descripción
Aplicación web desarrollada con Spring Boot que permite gestionar avisos de adopción de mascotas con sistema de evaluación mediante notas.

## Tecnologías Utilizadas
- **Backend:** Spring Boot 3.2.0, Java 17
- **Base de datos:** MySQL 8.0
- **ORM:** Spring Data JPA / Hibernate
- **Frontend:** Thymeleaf, HTML5, CSS3, JavaScript (Fetch API)
- **Build Tool:** Maven 3.9.11

## Requisitos
- Java JDK 17 o superior
- Maven 3.6+
- MySQL 8.0
- Base de datos `tarea2` configurada

## Configuración de Base de Datos
```sql
Usuario: cc5002
Contraseña: programacionweb
Base de datos: tarea2
```

## Instalación y Ejecución

### 1. Clonar o descargar el proyecto

### 2. Configurar la base de datos
Asegúrate de que MySQL esté corriendo y la base de datos `tarea2` exista con la tabla `nota` creada.

### 3. Compilar el proyecto
```bash
mvn clean install
```

### 4. Ejecutar la aplicación
```bash
mvn spring-boot:run
```

### 5. Acceder a la aplicación
Abre tu navegador en: `http://localhost:8080`

## Funcionalidades Implementadas

### ✅ [2 puntos] Listado de Avisos
- Muestra tabla con columnas: ID, Fecha publicación, Sector, Cantidad Tipo Edad, Comuna, Nota
- La columna "nota" presenta el promedio de evaluaciones
- Muestra "-" si el aviso no tiene notas

### ✅ [3 puntos] Evaluación de Avisos
- Al hacer clic en "evaluar", solicita una nota entre 1 y 7
- Valida que sea número entero entre 1 y 7 (inclusivo)
- Guarda la nota en la base de datos
- Validación del lado del cliente y del servidor

### ✅ [1 punto] Actualización Asíncrona
- Llamada asíncrona con JavaScript (Fetch API)
- Recalcula y actualiza el promedio sin recargar la página
- Animación visual al actualizar el promedio

## Estructura del Proyecto
```
src/
├── main/
│   ├── java/com/uchile/cc5002/avisos/
│   │   ├── AvisosAdopcionApplication.java
│   │   ├── controller/
│   │   │   ├── AvisoController.java
│   │   │   └── NotaRestController.java
│   │   ├── entity/
│   │   │   ├── AvisoAdopcion.java
│   │   │   ├── Comuna.java
│   │   │   ├── Nota.java
│   │   │   └── Region.java
│   │   ├── repository/
│   │   │   ├── AvisoAdopcionRepository.java
│   │   │   └── NotaRepository.java
│   │   ├── service/
│   │   │   └── NotaService.java
│   │   └── dto/
│   │       └── AvisoDTO.java
│   └── resources/
│       ├── application.properties
│       ├── templates/
│       │   └── listado-avisos.html
│       └── static/
│           ├── css/
│           │   └── estilos.css
│           └── js/
│               └── evaluacion.js
└── test/
```

## Endpoints

### Vista Web
- `GET /` - Listado de avisos de adopción

### API REST
- `POST /api/avisos/{avisoId}/notas` - Agregar una nota a un aviso
  - Body: `{ "nota": <1-7> }`
  - Response: `{ "success": true, "promedio": <número>, "promedioFormateado": "<texto>" }`

## Validaciones Implementadas
- **Cliente (JavaScript):**
  - Validación de que la nota sea un número
  - Validación del rango 1-7
  - Validación de que sea entero

- **Servidor (Java):**
  - Validación del rango 1-7
  - Manejo de errores
  - Respuestas JSON estructuradas

## Notas de Implementación
- Se utilizó Lombok para reducir código boilerplate
- JPA mapea automáticamente las entidades a las tablas existentes
- El promedio se calcula en tiempo real con cada evaluación
- Las llamadas asíncronas usan Fetch API (JavaScript moderno)
