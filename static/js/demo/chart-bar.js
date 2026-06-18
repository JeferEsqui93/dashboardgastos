document.addEventListener("DOMContentLoaded", function () {
    var ctx = document.getElementById("myBarChart");
    
    // Si la gráfica no está en la página actual (ej: estás en Login), frena el script
    if (!ctx) return;

    // Captura dinámica de tus datos reales desde el HTML
    var etiquetas = JSON.parse(ctx.getAttribute("data-etiquetas"));
    var valores = JSON.parse(ctx.getAttribute("data-valores"));

    // Inicializamos tu gráfico con el estilo exacto que te gusta
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: etiquetas, // <--- Dinámico
            datasets: [{
                label: "Total Gastado $",
                backgroundColor: "#4e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
                data: valores, // <--- Dinámico
                maxBarThickness: 50 // <--- AGREGA ESTA LÍNEA (Ajusta el número a tu gusto, ej: 20 o 30)
            }],
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    gridLines: { display: false, drawBorder: false },
                    ticks: { maxTicksLimit: 10 }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) { return '$' + value.toLocaleString(); }
                    }
                }]
            },
            legend: { display: false },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        return "Total: $" + tooltipItem.yLabel.toLocaleString();
                    }
                }
            }
        }
    });
});