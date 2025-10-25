// comentarios.js - Manejo de comentarios con llamadas asíncronas

document.addEventListener('DOMContentLoaded', function() {
    // Cargar comentarios al iniciar
    cargarComentarios();
    
    // Manejar envío del formulario
    document.getElementById('form-comentario').addEventListener('submit', enviarComentario);
});

/**
 * Carga y muestra los comentarios del aviso (LLAMADA ASÍNCRONA GET)
 */
function cargarComentarios() {
    fetch(`/api/aviso/${AVISO_ID}/comentarios`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar comentarios');
            }
            return response.json();
        })
        .then(comentarios => {
            mostrarComentarios(comentarios);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('comentarios-contenedor').innerHTML = 
                '<p class="error">Error al cargar los comentarios</p>';
        });
}

/**
 * Muestra los comentarios en el DOM
 */
function mostrarComentarios(comentarios) {
    const contenedor = document.getElementById('comentarios-contenedor');
    
    if (comentarios.length === 0) {
        contenedor.innerHTML = '<p class="sin-comentarios">No hay comentarios todavía. ¡Sé el primero en comentar!</p>';
        return;
    }
    
    let html = '';
    comentarios.forEach(comentario => {
        html += `
            <div class="comentario">
                <div class="comentario-header">
                    <strong class="comentario-nombre">${escapeHtml(comentario.nombre)}</strong>
                    <span class="comentario-fecha">${comentario.fecha}</span>
                </div>
                <div class="comentario-texto">
                    ${escapeHtml(comentario.texto)}
                </div>
            </div>
        `;
    });
    
    contenedor.innerHTML = html;
}

/**
 * Envía un nuevo comentario al servidor (LLAMADA ASÍNCRONA POST)
 */
function enviarComentario(e) {
    e.preventDefault(); // Prevenir envío tradicional del formulario
    
    // Limpiar mensajes de error previos
    limpiarErrores();
    
    // Obtener valores del formulario
    const nombre = document.getElementById('nombre-comentario').value.trim();
    const texto = document.getElementById('texto-comentario').value.trim();
    
    // Validar en el cliente
    const errores = validarComentario(nombre, texto);
    
    if (Object.keys(errores).length > 0) {
        mostrarErrores(errores);
        return;
    }
    
    // Deshabilitar botón mientras se envía
    const btnEnviar = document.getElementById('btn-enviar');
    btnEnviar.disabled = true;
    btnEnviar.textContent = 'Enviando...';
    
    // Enviar al servidor
    fetch(`/api/aviso/${AVISO_ID}/comentario`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: nombre,
            texto: texto
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Éxito: limpiar formulario y recargar comentarios
            document.getElementById('form-comentario').reset();
            mostrarMensajeExito('¡Comentario agregado exitosamente!');
            cargarComentarios(); // Recargar lista
        } else {
            // Error del servidor
            if (data.errores) {
                mostrarErrores(data.errores);
            } else {
                mostrarMensajeError(data.error || 'Error al agregar el comentario');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarMensajeError('Error de conexión. Intenta nuevamente.');
    })
    .finally(() => {
        // Rehabilitar botón
        btnEnviar.disabled = false;
        btnEnviar.textContent = 'Agregar comentario';
    });
}

/**
 * Valida los datos del comentario
 */
function validarComentario(nombre, texto) {
    const errores = {};
    
    // Validar nombre
    if (!nombre) {
        errores.nombre = 'El nombre es obligatorio';
    } else if (nombre.length < 3) {
        errores.nombre = 'El nombre debe tener al menos 3 caracteres';
    } else if (nombre.length > 80) {
        errores.nombre = 'El nombre no puede superar 80 caracteres';
    }
    
    // Validar texto
    if (!texto) {
        errores.texto = 'El comentario es obligatorio';
    } else if (texto.length < 5) {
        errores.texto = 'El comentario debe tener al menos 5 caracteres';
    }
    
    return errores;
}

/**
 * Muestra errores de validación en el formulario
 */
function mostrarErrores(errores) {
    if (errores.nombre) {
        const errorNombre = document.getElementById('error-nombre');
        errorNombre.textContent = errores.nombre;
        errorNombre.style.display = 'block';
    }
    
    if (errores.texto) {
        const errorTexto = document.getElementById('error-texto');
        errorTexto.textContent = errores.texto;
        errorTexto.style.display = 'block';
    }
}

/**
 * Limpia todos los mensajes de error
 */
function limpiarErrores() {
    document.getElementById('error-nombre').style.display = 'none';
    document.getElementById('error-texto').style.display = 'none';
    document.getElementById('mensaje-comentario').innerHTML = '';
}

/**
 * Muestra un mensaje de éxito
 */
function mostrarMensajeExito(mensaje) {
    const div = document.getElementById('mensaje-comentario');
    div.innerHTML = `<p class="success">${mensaje}</p>`;
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        div.innerHTML = '';
    }, 3000);
}

/**
 * Muestra un mensaje de error
 */
function mostrarMensajeError(mensaje) {
    const div = document.getElementById('mensaje-comentario');
    div.innerHTML = `<p class="error">${mensaje}</p>`;
}

/**
 * Escapa HTML para prevenir XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}