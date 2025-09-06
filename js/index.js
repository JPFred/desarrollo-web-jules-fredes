// --- Redireccionador del index ---

document.addEventListener('DOMContentLoaded', function() {
    const botones = document.querySelectorAll('.button');

    function redireccionar(pag) {
        console.log('Redirigiendo a:', pag + '.html');
        window.location.href = pag + '.html';
    }

    botones.forEach((boton) => {
        boton.addEventListener('click', () => {
            const pag = boton.id;
            console.log('Botón clickeado:', pag);
            redireccionar(pag);
        });
    });
});


