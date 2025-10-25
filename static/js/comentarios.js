// --- Sistema de comentarios ---

document.addEventListener('DOMContentLoaded', function() {
    cargarComentarios();
    document.getElementById('form-comentario').addEventListener('submit', enviarComentario);
});

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

function enviarComentario(e) {
    e.preventDefault();
    
    limpiarErrores();
    
    const nombre = document.getElementById('nombre-comentario').value.trim();
    const texto = document.getElementById('texto-comentario').value.trim();
    
    const errores = validarComentario(nombre, texto);
    
    if (Object.keys(errores).length > 0) {
        mostrarErrores(errores);
        return;
    }
    
    const btnEnviar = document.getElementById('btn-enviar');
    btnEnviar.disabled = true;
    btnEnviar.textContent = 'Enviando...';
    
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
            document.getElementById('form-comentario').reset();
            mostrarMensajeExito('¡Comentario agregado exitosamente!');
            cargarComentarios();
        } else {
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
        btnEnviar.disabled = false;
        btnEnviar.textContent = 'Agregar comentario';
    });
}

function validarComentario(nombre, texto) {
    const errores = {};
    
    if (!nombre) {
        errores.nombre = 'El nombre es obligatorio';
    } else if (nombre.length < 3) {
        errores.nombre = 'El nombre debe tener al menos 3 caracteres';
    } else if (nombre.length > 80) {
        errores.nombre = 'El nombre no puede superar 80 caracteres';
    }
    
    if (!texto) {
        errores.texto = 'El comentario es obligatorio';
    } else if (texto.length < 5) {
        errores.texto = 'El comentario debe tener al menos 5 caracteres';
    }
    
    return errores;
}

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

function limpiarErrores() {
    document.getElementById('error-nombre').style.display = 'none';
    document.getElementById('error-texto').style.display = 'none';
    document.getElementById('mensaje-comentario').innerHTML = '';
}

function mostrarMensajeExito(mensaje) {
    const div = document.getElementById('mensaje-comentario');
    div.innerHTML = `<p class="success">${mensaje}</p>`;
    
    setTimeout(() => {
        div.innerHTML = '';
    }, 3000);
}

function mostrarMensajeError(mensaje) {
    const div = document.getElementById('mensaje-comentario');
    div.innerHTML = `<p class="error">${mensaje}</p>`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}