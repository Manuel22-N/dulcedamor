document.addEventListener("DOMContentLoaded", function () {
    // Establecer la fecha actual en todos los campos de fecha
    const fechaInputs = document.querySelectorAll('.fecha_actual');
    const today = new Date().toISOString().split("T")[0];
    fechaInputs.forEach(input => input.value = today);

    // Delegación de eventos para manejar la búsqueda de productos
    document.querySelectorAll('#tbl_globos, #tbl_empaques, #tbl_alimentos, #tbl_bases').forEach(tabla => {
        tabla.querySelector('tbody').addEventListener('input', function (event) {
            if (event.target.classList.contains('buscar_producto')) {
                const input = event.target;
                const tabla = input.getAttribute("data-tabla");
                const codigo = input.value;
                const productoNombre = input.closest('tr').querySelector('.producto_nombre');

                if (codigo) {
                    fetch(`/desayunos/buscar_producto/${codigo}/`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                productoNombre.textContent = data.nombre;
                            } else {
                                productoNombre.textContent = "Producto no encontrado";
                            }
                        })
                        .catch(error => console.error("Error:", error));
                } else {
                    productoNombre.textContent = "";
                }
            }
        });
    });

    // Función para agregar una nueva fila
    document.querySelectorAll('.agregar_fila').forEach(function (button) {
        button.addEventListener('click', function () {
            let tabla = this.dataset.tabla;
            let filaNueva = document.createElement('tr');

            // Crear la nueva fila con los mismos campos
            filaNueva.innerHTML = ` 
                <td><input type="text" class="form-control buscar_producto" data-tabla="${tabla}" placeholder="Código del producto"></td>
                <td><span class="producto_nombre"></span></td>
                <td><input type="number" class="form-control cantidad_producto" value="1" min="1" step="1"></td>
                <td><input type="date" class="form-control fecha_actual" value="${today}"></td>
                <td><button type="button" class="btn btn-danger btn-sm eliminar_fila"><i class="fas fa-trash"></i></button></td>
            `;

            // Agregar la nueva fila a la tabla correspondiente
            document.querySelector(`#tbl_${tabla} tbody`).appendChild(filaNueva);

            // Event listener para eliminar la fila
            filaNueva.querySelector('.eliminar_fila').addEventListener('click', function () {
                filaNueva.remove();
            });
        });
    });

    // --- Evento para guardar el desayuno ---
    document.getElementById("guardar_desayuno").addEventListener("click", function () {
        const tablas = ["globos", "empaques", "alimentos", "bases"];
        let datos = [];
    
        tablas.forEach(tabla => {
            const filas = document.querySelectorAll(`#tbl_${tabla} tbody tr`);
            filas.forEach(fila => {
                const codigo = fila.querySelector(".buscar_producto").value.trim();
                const cantidad = parseInt(fila.querySelector(".cantidad_producto").value, 10);
                if (codigo && cantidad > 0) {
                    datos.push({ tabla, codigo, cantidad });
                }
            });
        });
    
        if (datos.length === 0) {
            mostrarMensaje("warning", "No se han agregado productos en ninguna tabla.");
            return;
        }
    
        // Enviar los datos al backend
        fetch("/desayunos/guardar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ productos: datos }),
        })
            .then(response => response.json())
            .then(data => {
                const messageContainer = document.getElementById("message-container");
                messageContainer.innerHTML = ""; // Limpiar mensajes previos
            
                const message = document.createElement("div");
                message.classList.add("alert", "mt-3"); // Estilo básico del mensaje
                if (data.success) {
                    message.classList.add("alert-success");
                    message.textContent = data.mensaje;

                    // Si la operación fue exitosa, limpiar las tablas
                    tablas.forEach(tabla => {
                        const tbody = document.querySelector(`#tbl_${tabla} tbody`);
                        tbody.querySelectorAll("tr:not(:first-child)").forEach(fila => fila.remove());
                    });
                } else {
                    message.classList.add("alert-danger");
                    message.textContent = data.mensaje; // Mostrar el mensaje de error detallado
                }
            
                messageContainer.appendChild(message);
            
                // Eliminar el mensaje después de 5 segundos
                setTimeout(() => {
                    message.remove();
                }, 20000);
            })
            .catch(error => {
                mostrarMensaje("error", "Ocurrió un error al guardar los datos.");
                console.error("Error:", error);
            });
    });
    
    // Función para mostrar mensajes en el contenedor
    function mostrarMensaje(tipo, mensaje) {
        const container = document.getElementById("message-container");
        const colores = { success: "alert-success", error: "alert-danger", warning: "alert-warning" };
        container.innerHTML = `<div class="alert ${colores[tipo]}">${mensaje}</div>`;
    }

    // Función para obtener el CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
document.getElementById('btn-reporte').addEventListener('click', function() {
    var fecha = document.getElementById('fecha-reporte').value;

    if (!fecha) {
        alert("Por favor, selecciona una fecha.");
        return;
    }

    // Hacer la solicitud GET para generar el reporte
    fetch(`/reporte/?fecha=${fecha}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Reporte generado:", data.reporte);
            
            // Aquí puedes mostrar los datos del reporte
            // Por ejemplo, agregar los datos a una tabla HTML
            let reporte = data.reporte;
            let html = '<table class="table table-bordered"><thead><tr><th>Producto</th><th>Cantidad</th><th>Fecha</th><th>Usuario</th><th>Precio</th></tr></thead><tbody>';
            reporte.forEach(item => {
                html += `<tr>
                            <td>${item.producto}</td>
                            <td>${item.cantidad}</td>
                            <td>${item.fecha}</td>
                            <td>${item.usuario}</td>
                            <td>${item.precio}</td>
                        </tr>`;
            });
            html += '</tbody></table>';

            // Mostrar el reporte en el contenedor
            document.getElementById('message-container').innerHTML = html;
        } else {
            alert(data.mensaje);
        }
    })
    .catch(error => {
        console.error("Error al generar el reporte:", error);
        alert("Hubo un error al generar el reporte.");
    });
});

document.getElementById('generar_reporte').addEventListener('click', function () {
    const fecha = document.getElementById('fecha_reporte').value;  // Obtener fecha seleccionada
    if (fecha) {
        // Redirigir a la vista para generar el reporte en PDF
        window.location.href = `/reporte/?fecha=${fecha}`;
    } else {
        alert('Por favor, selecciona una fecha.');
    }
});