(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Seguro de eliminar la conexion Mqtt?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
    
})();