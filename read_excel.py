import pandas as pd
import math
from pydantic import BaseModel, field_validator
from typing import Optional
from database import ids_validos


# modelo de pydantic

class Producto(BaseModel):
    id: Optional[int]
    nombre_producto: str
    categoria: str
    marca: str
    descripcion: str
    stock_actual: int
    costo_unitario: float
    precio_venta: float

    @field_validator("id")
    @classmethod
    def validar_id(cls, v: int) -> int:
        if not v in ids_validos():
            raise ValueError("El id no corresponde con ningun producto")
        return v


class Productos(BaseModel):
    productos: list[Producto]


def leer_excel(file):
    df = pd.read_excel(file)
    return df


def validar_df(df):

    if df.empty or df.columns.empty:
        raise ValueError("El Excel se encuentra vacío")

    # transformar los nombres de las columnas a string para poder validarlas
    columnas = [str(c).strip().lower() for c in df.columns]
    df.columns = columnas

    # validar nombre de las columnas
    columnas_esperadas = {"id", "nombre_producto", "categoria", "marca",
                          "descripcion", "stock_actual", "costo_unitario", "precio_venta"}
    if not columnas_esperadas.issubset(columnas):
        raise ValueError("Faltan columnas requeridas en el Excel")
    return df

# Función para reemplazar NaN por None


def nan_to_none(d):
    return {k: (None if (isinstance(v, float) and math.isnan(v)) else v)
            for k, v in d.items()}


def crear_diccionario(df):
    productos_dict = df.to_dict(orient="records")
    # reamplazamos Nan por None para evitar error en la validacion con pydantic
    productos_dict = [nan_to_none(d) for d in productos_dict]
    return productos_dict


def validar_tipos(productos_dict):
    productos = Productos(productos=productos_dict)
    return productos.productos
