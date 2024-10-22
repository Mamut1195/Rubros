document.addEventListener("DOMContentLoaded", function () {
    // Función para calcular el costo por unidad
    function calcularCostoPorUnidad() {
        const cantidadInput = document.querySelector("#id_cantidad");  // Campo de cantidad
        const costoInput = document.querySelector("#id_costo");  // Campo de costo total
        const costoPorUnidadInput = document.querySelector("#id_costo_por_unidad");  // Campo de costo por unidad

        // Escuchar cambios en los campos de cantidad y costo
        [cantidadInput, costoInput].forEach(function (input) {
            input.addEventListener("input", function () {
                const cantidad = parseFloat(cantidadInput.value);
                const costo = parseFloat(costoInput.value);

                if (!isNaN(cantidad) && cantidad > 0 && !isNaN(costo)) {
                    // Calcular el costo por unidad y asignarlo al campo de solo lectura
                    const costoPorUnidad = (costo / cantidad).toFixed(2);
                    costoPorUnidadInput.value = costoPorUnidad;
                } else {
                    costoPorUnidadInput.value = "";
                }
            });
        });
    }

    // Llama a la función para actualizar el costo por unidad en tiempo real
    calcularCostoPorUnidad();
});
