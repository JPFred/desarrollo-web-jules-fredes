/**
 * Función para evaluar un aviso de adopción
 * Solicita una nota al usuario y la envía de forma asíncrona al servidor
 */
function evaluarAviso(event) {
    event.preventDefault();
    
    const avisoId = event.target.getAttribute('data-aviso-id');
    
    // Solicitar nota al usuario
    const notaInput = prompt('Ingrese una nota entre 1 y 7 para este aviso:');
    
    // Validar que se ingresó algo
    if (notaInput === null || notaInput.trim() === '') {
        return; // Usuario canceló o no ingresó nada
    }
    
    // Convertir a número entero
    const nota = parseInt(notaInput.trim());
    
    // Validar que sea un número entero entre 1 y 7
    if (isNaN(nota) || nota < 1 || nota > 7 || !Number.isInteger(parseFloat(notaInput.trim()))) {
        alert('Error: La nota debe ser un número entero entre 1 y 7');
        return;
    }
    
    // Enviar nota de forma asíncrona usando fetch
    fetch(`/api/avisos/${avisoId}/notas`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nota: nota })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar el promedio en la interfaz
            actualizarPromedio(avisoId, data.promedioFormateado);
            alert(`Nota agregada exitosamente. Nuevo promedio: ${data.promedioFormateado}`);
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error al agregar la nota:', error);
        alert('Error al comunicarse con el servidor. Por favor, intente nuevamente.');
    });
}

/**
 * Actualiza el promedio mostrado en la tabla
 */
function actualizarPromedio(avisoId, nuevoPromedio) {
    const celdaPromedio = document.querySelector(
        `.promedio-cell[data-aviso-id="${avisoId}"] .promedio-value`
    );
    
    if (celdaPromedio) {
        // Animación simple de actualización
        celdaPromedio.style.transition = 'all 0.3s';
        celdaPromedio.style.transform = 'scale(1.2)';
        celdaPromedio.style.color = '#4CAF50';
        
        // Actualizar el valor
        celdaPromedio.textContent = nuevoPromedio;
        
        // Volver al estado normal
        setTimeout(() => {
            celdaPromedio.style.transform = 'scale(1)';
            celdaPromedio.style.color = '';
        }, 300);
    }
}
