function actualizar() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("ocupacion").innerHTML = 
                "Vehículos dentro: " + data.ocupacion;

            document.getElementById("libres").innerHTML = 
                "Espacios libres: " + data.libres;

            document.getElementById("capacidad").innerHTML = 
                "Capacidad: " + data.capacidad;
        });
}

// Actualizar cada 1 segundo
setInterval(actualizar, 1000);
actualizar();
