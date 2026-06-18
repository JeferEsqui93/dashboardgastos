// Asegúrate de que esto corra dentro del mismo evento "DOMContentLoaded" de tu archivo
var ctxPie = document.getElementById("myPieChart");

if (ctxPie) {
    var etiquetasPie = JSON.parse(ctxPie.getAttribute("data-etiquetas"));
    var valoresPie = JSON.parse(ctxPie.getAttribute("data-valores"));

    // MEJORA 1: Paleta de colores extendida por si hay muchas categorías
    var paletaColores = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796', '#5a5c69', '#f8f9fc'];
    var paletaHover = ['#2e59d9', '#17a673', '#2c9faf', '#dda20a', '#be2617', '#6e707e', '#3a3b45', '#dfe4ec'];

    // Asegurar que haya suficientes colores repitiendo la paleta si es necesario
    var bgColores = etiquetasPie.map((_, i) => paletaColores[i % paletaColores.length]);
    var bgHover = etiquetasPie.map((_, i) => paletaHover[i % paletaHover.length]);

    // Calcular la sumatoria total de los gastos para obtener los porcentajes
    var totalGastos = valoresPie.reduce((a, b) => a + b, 0);

    var myPieChart = new Chart(ctxPie, {
        type: 'doughnut',
        data: {
            labels: etiquetasPie,
            datasets: [{
                data: valoresPie,
                backgroundColor: bgColores,
                hoverBackgroundColor: bgHover,
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }],
        },
        options: {
            maintainAspectRatio: false,
            layout: {
        padding: {
            top: 10,
            bottom: 15,
            left: 10,
            right: 10
        }
    },
    legend: {
        display: true,
        position: 'bottom',
        labels: { boxWidth: 15 }
    },
    cutoutPercentage: 75,
            legend: {
                display: true, // Activamos la leyenda para saber qué color es cada categoría
                position: 'bottom',
                labels: { boxWidth: 15 }
            },
            cutoutPercentage: 75, // Ajustado sutilmente para que se vea más estilizado
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: true, // Muestra el cuadrito de color en el tooltip
                caretPadding: 10,
                callbacks: {
                    // MEJORA 2: Tooltip dinámico que muestra Valor + Porcentaje
                    label: function(tooltipItem, data) {
                        var valorActual = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var etiquetaActual = data.labels[tooltipItem.index];
                        
                        // Calcular porcentaje
                        var porcentaje = totalGastos > 0 ? ((valorActual / totalGastos) * 100).toFixed(1) : 0;                        
                        return etiquetaActual + ": $" + valorActual.toLocaleString() + " (" + porcentaje + "%)";
                    }
                }
            },
        },
    });
}