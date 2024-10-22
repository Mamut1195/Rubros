document.addEventListener('DOMContentLoaded', function () {
    const esAlquiladoField = document.querySelector('#id_es_alquilado');
    const costoAlquilerField = document.querySelector('#id_costo_alquiler');
    const tipoAlquilerField = document.querySelector('#id_tipo_alquiler');

    function toggleAlquilerFields() {
        if (esAlquiladoField.checked) {
            costoAlquilerField.disabled = false;
            tipoAlquilerField.disabled = false;
        } else {
            costoAlquilerField.disabled = true;
            tipoAlquilerField.disabled = true;
        }
    }

    // Inicializar el estado de los campos
    toggleAlquilerFields();

    // Escuchar cambios en el campo "es_alquilado"
    esAlquiladoField.addEventListener('change', toggleAlquilerFields);
});
