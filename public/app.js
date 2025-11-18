const form = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) preview.textContent = `Archivo seleccionado: ${file.name}`;
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = fileInput.files[0];
  if (!file) return alert("Selecciona un archivo primero.");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(
    "https://inventario-con-excel.onrender.com/subir-excel",
    {
      method: "POST",
      body: formData,
    }
  );

  if (res.ok) {
    alert("Archivo subido correctamente.");
  } else {
    alert("Error al subir el archivo.");
  }
});

function refresh() {
  const tbody = document.querySelector("#table tbody");
  tbody.innerHTML = "";
  fetch("https://inventario-con-excel.onrender.com/productos")
    .then((response) => response.json())
    .then((data) => {
      const tbody = document.querySelector("#table tbody");
      data.forEach((item) => {
        const fila = document.createElement("tr");

        const celda1 = document.createElement("td");
        celda1.textContent = item.id_producto;
        const celda2 = document.createElement("td");
        celda2.textContent = item.nombre_producto;
        const celda3 = document.createElement("td");
        celda3.textContent = item.categoria;
        const celda4 = document.createElement("td");
        celda4.textContent = item.marca;
        const celda5 = document.createElement("td");
        celda5.textContent = item.descripcion;
        const celda6 = document.createElement("td");
        celda6.textContent = item.stock_actual;
        const celda7 = document.createElement("td");
        celda7.textContent = item.costo_unitario;
        const celda8 = document.createElement("td");
        celda8.textContent = item.precio_venta;

        fila.appendChild(celda1);
        fila.appendChild(celda2);
        fila.appendChild(celda3);
        fila.appendChild(celda4);
        fila.appendChild(celda5);
        fila.appendChild(celda6);
        fila.appendChild(celda7);
        fila.appendChild(celda8);

        tbody.appendChild(fila);
        console.log(data);
      });
    })
    .catch((error) => console.error("Error al cargar los datos:", error));
}

document.getElementById("refresh").addEventListener("click", refresh);

function download() {
  fetch("https://inventario-con-excel.onrender.com/exportar-excel")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al obtener el archivo");
      }
      return response.blob();
    })
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "productos.xlsx";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      window.URL.revokeObjectURL(url);
    })
    .catch((error) => console.error("Error al exportar los datos:", error));
}

document.getElementById("download").addEventListener("click", download);
