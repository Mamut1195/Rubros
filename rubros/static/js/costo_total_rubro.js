document.addEventListener("DOMContentLoaded", function() {
    // Obtén los elementos para el costo total de materiales, herramientas y mano de obra por id
    const costoTotalMaterialesElement = document.querySelector('.form-row.field-get_costo_total_materiales .readonly');
    const costoTotalHerramientasElement = document.querySelector('.form-row.field-get_costo_total_herramientas .readonly');
    const costoTotalManoObraElement = document.querySelector('.form-row.field-get_costo_total_mano_de_obra .readonly');
    const indirectos = document.getElementById('id_indirectos').value;

    // Verifica que los elementos de costo estén presentes y obtén sus valores de texto
    const costoTotalMateriales = costoTotalMaterialesElement ? parseFloat(costoTotalMaterialesElement.textContent.trim()) : 0;
    const costoTotalHerramientas = costoTotalHerramientasElement ? parseFloat(costoTotalHerramientasElement.textContent.trim()) : 0;
    const costoTotalManoObra = costoTotalManoObraElement ? parseFloat(costoTotalManoObraElement.textContent.trim()) : 0;

    // Calcula la suma subtotal
    const sumaSubTotal = costoTotalMateriales + costoTotalHerramientas + costoTotalManoObra;

    //Calculo de indirectos
    const indirectosTotal = sumaSubTotal * indirectos/100;
    
    //Calculo total
    const totalRubro = indirectosTotal + sumaSubTotal;

    const indirectosrow = document.createElement('div');
    indirectosrow.textContent = `Total del Indirectos: ${indirectosTotal.toFixed(2)}`; // Mostrar con dos decimales
    indirectosrow.style.marginTop = "15px";
    indirectosrow.style.textAlign = "right";
    indirectosrow.style.marginRight = "10em";
    indirectosrow.style.padding = "15px"; // Añade relleno dentro del box
    indirectosrow.style.backgroundColor = "#121c4bad"; // Fondo azul
    indirectosrow.style.color = "white"; // Texto blanco para contraste
    indirectosrow.style.width = "98%"; // Ocupa todo el ancho del contenedor
    indirectosrow.style.fontSize = "1.1em"; // Tamaño de fuente más grande
    indirectosrow.style.borderBottom = "2px solid #ffffff";
    indirectosrow.style.borderColor = '#121939d9';


    // Crea un elemento para mostrar la suma subtotal
    const subtotalRow = document.createElement("div");
    subtotalRow.textContent = `Subtotal APU: ${sumaSubTotal.toFixed(2)}`; // Mostrar con dos decimales
    subtotalRow.style.textAlign = "right";
    subtotalRow.style.marginRight = "10em";
    subtotalRow.style.padding = "15px"; // Añade relleno dentro del box
    subtotalRow.style.backgroundColor = "#121c4bad"; // Fondo azul
    subtotalRow.style.color = "white"; // Texto blanco para contraste
    subtotalRow.style.width = "98%"; // Ocupa todo el ancho del contenedor
    subtotalRow.style.fontSize = "1.1em"; // Tamaño de fuente más grande
    subtotalRow.style.borderBottom = "2px solid #ffffff";
    subtotalRow.style.borderColor = '#121939d9';

    const totalRow = document.createElement("div");
    totalRow.textContent = `Total APU: ${totalRubro.toFixed(2)}`; // Mostrar con dos decimales
    totalRow.style.fontWeight = "bold";
    totalRow.style.textAlign = "right";
    totalRow.style.marginRight = "10em";
    totalRow.style.padding = "15px"; // Añade relleno dentro del box
    totalRow.style.backgroundColor = "#121c4b"; // Fondo azul
    totalRow.style.color = "white"; // Texto blanco para contraste
    totalRow.style.width = "98%"; // Ocupa todo el ancho del contenedor
    totalRow.style.fontSize = "1.1em"; // Tamaño de fuente más grande


    // Agrega el total sumado al final del contenido
    const container = document.getElementById("rubromanoobra_set-group"); // Cambia este ID si el contenedor es diferente
    if (container) {
        container.appendChild(indirectosrow);
        container.appendChild(subtotalRow);
        container.appendChild(totalRow);

    }
});
