from read_excel import leer_excel, validar_df, crear_diccionario, validar_tipos
from database import ids_validos, ver_productos
import math


# df = leer_excel("inventario.xlsx")
# df = validar_df(df)
# productos = crear_diccionario(df)
# productos = validar_tipos(productos)

# print(productos)

productos = ver_productos()
print(productos)
