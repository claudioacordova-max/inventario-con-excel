# run with: uvicorn main:app --reload
from fastapi import FastAPI, UploadFile, File, HTTPException, responses
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import agregar_productos, ver_productos
from read_excel import leer_excel, validar_df, crear_diccionario, validar_tipos, generar_excel_productos


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="public"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("public/index.html")


@app.get("/productos", tags=["Excel"])
def get_productos():
    return ver_productos()


@app.post("/subir-excel", tags=["Excel"])
async def post_subir_excel(file: UploadFile = File(...)):
    tipos_validos = [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel"
    ]

    # Error 415: Tipo de archivo no soportado
    if file.content_type not in tipos_validos:
        raise HTTPException(
            status_code=415,
            detail="El archivo debe ser un Excel (.xlsx o .xls)"
        )

    try:
        contenido = await file.read()
        df = leer_excel(contenido)
        df = validar_df(df)
        productos = crear_diccionario(df)
        productos = validar_tipos(productos)
        agregar_productos(productos)

        # Código 201: creado exitosamente
        return JSONResponse(
            status_code=201,
            content={"message": "Excel cargado correctamente"}
        )

    except ValueError as ve:
        # Error 400: datos inválidos
        raise HTTPException(
            status_code=400,
            detail=f"Error de validación: {str(ve)}"
        )

    except Exception as e:
        # Error 500: error interno del servidor
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@app.get("/exportar-excel/")
async def exportar_excel():
    archivo_excel = generar_excel_productos()

    return StreamingResponse(
        archivo_excel,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=productos.xlsx"}
    )
