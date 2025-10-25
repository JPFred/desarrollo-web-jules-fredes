// --- Gráficos de estadísticas ---

document.addEventListener('DOMContentLoaded', function() {
    cargarResumenGeneral();
    cargarGraficoLineas();
    cargarGraficoTorta();
    cargarGraficoBarras();
});

function cargarResumenGeneral() {
    fetch('/api/estadisticas/avisos-por-tipo')
        .then(response => response.json())
        .then(datos => {
            let totalGatos = 0;
            let totalPerros = 0;
            
            datos.forEach(item => {
                if (item.tipo === 'gato') {
                    totalGatos = item.cantidad;
                } else if (item.tipo === 'perro') {
                    totalPerros = item.cantidad;
                }
            });
            
            const totalAvisos = totalGatos + totalPerros;
            
            document.getElementById('total-avisos').textContent = totalAvisos;
            document.getElementById('total-gatos').textContent = totalGatos;
            document.getElementById('total-perros').textContent = totalPerros;
        })
        .catch(error => {
            console.error('Error al cargar resumen:', error);
        });
}

// Gráfico 1: Líneas - Avisos por día
function cargarGraficoLineas() {
    fetch('/api/estadisticas/avisos-por-dia')
        .then(response => response.json())
        .then(datos => {
            const fechas = datos.map(d => formatearFecha(d.fecha));
            const cantidades = datos.map(d => d.cantidad);
            
            const ctx = document.getElementById('grafico-lineas').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: fechas,
                    datasets: [{
                        label: 'Avisos de Adopción',
                        data: cantidades,
                        borderColor: '#d74967',
                        backgroundColor: 'rgba(215, 73, 103, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#d74967',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Avisos de Adopción por Día',
                            font: {
                                size: 18,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        legend: {
                            display: true,
                            position: 'top'
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            titleFont: {
                                size: 14
                            },
                            bodyFont: {
                                size: 13
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1,
                                font: {
                                    size: 12
                                }
                            },
                            title: {
                                display: true,
                                text: 'Cantidad de Avisos',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        },
                        x: {
                            ticks: {
                                maxRotation: 45,
                                minRotation: 45,
                                font: {
                                    size: 11
                                }
                            },
                            title: {
                                display: true,
                                text: 'Fecha',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error al cargar gráfico de líneas:', error);
            document.getElementById('grafico-lineas').insertAdjacentHTML('beforebegin', 
                '<p style="color: red; text-align: center;">Error al cargar el gráfico</p>');
        });
}

// Gráfico 2: Torta - Avisos por tipo
function cargarGraficoTorta() {
    fetch('/api/estadisticas/avisos-por-tipo')
        .then(response => response.json())
        .then(datos => {
            const tipos = datos.map(d => d.tipo === 'perro' ? 'Perros 🐶' : 'Gatos 🐱');
            const cantidades = datos.map(d => d.cantidad);
            
            const ctx = document.getElementById('grafico-torta').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: tipos,
                    datasets: [{
                        data: cantidades,
                        backgroundColor: [
                            '#f47066',
                            '#a7a6da'
                        ],
                        borderColor: '#fff',
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Avisos por Tipo de Mascota',
                            font: {
                                size: 18,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        legend: {
                            display: true,
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                font: {
                                    size: 14
                                }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error al cargar gráfico de torta:', error);
            document.getElementById('grafico-torta').insertAdjacentHTML('beforebegin', 
                '<p style="color: red; text-align: center;">Error al cargar el gráfico</p>');
        });
}

// Gráfico 3: Barras - Avisos por mes y tipo
function cargarGraficoBarras() {
    fetch('/api/estadisticas/avisos-por-mes-tipo')
        .then(response => response.json())
        .then(datos => {
            const meses = datos.map(d => formatearMes(d.mes));
            const cantidadPerros = datos.map(d => d.perros);
            const cantidadGatos = datos.map(d => d.gatos);
            
            const ctx = document.getElementById('grafico-barras').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: meses,
                    datasets: [
                        {
                            label: 'Perros 🐶',
                            data: cantidadPerros,
                            backgroundColor: '#f47066',
                            borderColor: '#e85a50',
                            borderWidth: 2
                        },
                        {
                            label: 'Gatos 🐱',
                            data: cantidadGatos,
                            backgroundColor: '#a7a6da',
                            borderColor: '#8f8ec5',
                            borderWidth: 2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Avisos por Mes y Tipo de Mascota',
                            font: {
                                size: 18,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                padding: 15,
                                font: {
                                    size: 14
                                }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1,
                                font: {
                                    size: 12
                                }
                            },
                            title: {
                                display: true,
                                text: 'Cantidad de Avisos',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        },
                        x: {
                            ticks: {
                                font: {
                                    size: 12
                                }
                            },
                            title: {
                                display: true,
                                text: 'Mes',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error al cargar gráfico de barras:', error);
            document.getElementById('grafico-barras').insertAdjacentHTML('beforebegin', 
                '<p style="color: red; text-align: center;">Error al cargar el gráfico</p>');
        });
}

function formatearFecha(fechaStr) {
    const fecha = new Date(fechaStr + 'T00:00:00');
    return fecha.toLocaleDateString('es-CL', { 
        day: '2-digit', 
        month: 'short', 
        year: 'numeric' 
    });
}

function formatearMes(mesStr) {
    const [year, month] = mesStr.split('-');
    const fecha = new Date(year, parseInt(month) - 1, 1);
    return fecha.toLocaleDateString('es-CL', { 
        month: 'long', 
        year: 'numeric' 
    });
}