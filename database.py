import sqlite3


def ver_productos():
    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM productos")
        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        productos = [dict(zip(columns, row)) for row in rows]
        return productos


def ids_validos():
    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT id_producto  FROM productos;")
        ids = [x[0] for x in cursor.fetchall()]
        ids.append(None)
        return ids


def agregar_productos(productos):
    productos_nuevos = [(
        p.nombre_producto, p.categoria, p.marca, p.descripcion,
        p.stock_actual, p.costo_unitario, p.precio_venta
    )
        for p in productos if p.id is None]

    nuevos_nombres = [(p.nombre_producto, p.id)
                      for p in productos if p.id is not None]
    nuevas_categorias = [(p.categoria, p.id)
                         for p in productos if p.id is not None]
    nuevas_marcas = [(p.marca, p.id)
                     for p in productos if p.id is not None]
    nuevas_descripciones = [(p.descripcion, p.id)
                            for p in productos if p.id is not None]
    nuevos_stocks_actuales = [(p.stock_actual, p.id)
                              for p in productos if p.id is not None]
    nuevos_costos_unitarios = [(p.costo_unitario, p.id)
                               for p in productos if p.id is not None]
    nuevos_precios_venta = [(p.precio_venta, p.id)
                            for p in productos if p.id is not None]

    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        cursor.executemany(
            """
            INSERT INTO productos (	
            nombre_producto,
            categoria,
            marca,
            descripcion,
            stock_actual,
            costo_unitario,
            precio_venta
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, productos_nuevos
        )
        cursor.executemany(
            "UPDATE productos SET nombre_producto = ? WHERE id_producto = ?", nuevos_nombres)
        cursor.executemany(
            "UPDATE productos SET categoria = ? WHERE id_producto = ?", nuevas_categorias)
        cursor.executemany(
            "UPDATE productos SET marca = ? WHERE id_producto = ?", nuevas_marcas)
        cursor.executemany(
            "UPDATE productos SET descripcion = ? WHERE id_producto = ?", nuevas_descripciones)
        cursor.executemany(
            "UPDATE productos SET stock_actual = ? WHERE id_producto = ?", nuevos_stocks_actuales)
        cursor.executemany(
            "UPDATE productos SET costo_unitario = ? WHERE id_producto = ?", nuevos_costos_unitarios)
        cursor.executemany(
            "UPDATE productos SET precio_venta = ? WHERE id_producto = ?", nuevos_precios_venta)
