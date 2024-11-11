document.addEventListener("DOMContentLoaded", function() {
    // Obtén el elemento de inline y el costo total de herramientas
    const inlineGroup = document.getElementById("rubroherramienta_set-group");
    const costoTotalElement = document.querySelector('.form-row.field-get_costo_total_herramientas .readonly');

    // Verifica que el elemento de costo total esté presente y obtén su contenido
    const totalCosto = costoTotalElement ? costoTotalElement.textContent.trim() : "0";

    // Crea un elemento para mostrar el total de herramientas
    const totalRow = document.createElement("div");
    totalRow.textContent = `Costo Total de Herramientas: ${totalCosto}`;
    totalRow.style.fontWeight = "bold";
    totalRow.style.marginTop = "10px";
    totalRow.style.textAlign = "right";
    totalRow.style.marginRight = "3em";

    // Añade el elemento después de los inlines
    if (inlineGroup) {
        inlineGroup.appendChild(totalRow);
    }
});
