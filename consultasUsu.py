import flet as ft
from pyairtable import Table

# Configuración de Airtable
AT_API_KEY = "patuASK11VeXlRg7q.95da8618bc32869c8ab41748d62e8ea5ce6fb29b4988ba5612f861a93061fc2b"
BASE_ID = "appO5xjRqKCWDWxyC"
TABLE_NAME = "usuario"

tabla = Table(AT_API_KEY, BASE_ID, TABLE_NAME)

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Consulta de usuarios"
    page.theme_mode = "light"
    page.window.width = 800
    page.window.height = 600
    page.appbar = ft.AppBar(
        title=ft.Text("Consulta de usuarios en la nube"),
        leading=ft.Icon("cloud"),
        center_title=True,
        bgcolor="blue",
        color="white"
    )

    # Encabezado de la tabla
    encabezado = [
        ft.DataColumn(ft.Text("Clave")),
        ft.DataColumn(ft.Text("Contraseña")),
        ft.DataColumn(ft.Text("Nombre completo")),
        ft.DataColumn(ft.Text("Es administrador"))
    ]

    # Obtener datos de Airtable
    filas = []
    try:
        registros = tabla.all()
        for d in registros:
            f = d["fields"]
            celda1 = ft.DataCell(ft.Text(f.get("clave", "")))
            celda2 = ft.DataCell(ft.Text(f.get("contra", "")))
            celda3 = ft.DataCell(ft.Text(f.get("nombre", "")))
            celda4 = ft.DataCell(ft.Text("Sí" if f.get("admin") else "No"))
            filas.append(ft.DataRow([celda1, celda2, celda3, celda4]))
    except Exception as e:
        page.add(ft.Text(f"Error al consultar usuarios: {e}", color="red"))
        return

    # Crear tabla
    tbl_usuarios = ft.DataTable(columns=encabezado, rows=filas)

    page.add(tbl_usuarios)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
