import flet as ft
from pyairtable import Table
from pyairtable.formulas import match

# Configuración de Airtable
AT_API_KEY = "patuASK11VeXlRg7q.95da8618bc32869c8ab41748d62e8ea5ce6fb29b4988ba5612f861a93061fc2b"
BASE_ID = "appO5xjRqKCWDWxyC"
TABLE_NAME = "usuario"

tabla = Table(AT_API_KEY, BASE_ID, TABLE_NAME)

def main(page: ft.Page):
    page.title = "Login"
    usuario = ft.TextField(label="Usuario", width=300)
    password = ft.TextField(label="Contraseña", password=True, width=300)
    mensaje = ft.Text()

    def login_click(e):
        try:
            formula = match({"clave": usuario.value, "contra": password.value})
            registro = tabla.first(formula=formula)
            if registro:
                mensaje.value = "Funciona!"
                page.go("/principal")
            else:
                mensaje.value = f"Usuario '{usuario.value}' no encontrado."
            page.update()
        except Exception as ex:
            mensaje.value = f"Error de Airtable: {ex}"
            page.update()

    page.add(
        usuario,
        password,
        ft.ElevatedButton("Ingresar", on_click=login_click),
        mensaje
    )

def principal(page: ft.Page):
    page.title = "Principal"
    page.add(
        ft.Text("Menú principal", size=30),
        ft.ElevatedButton("Agregar nuevo usuario", on_click=lambda e: page.go("/agregar_usuario")),
        ft.ElevatedButton("Consultar usuarios", on_click=lambda e: page.go("/consultar_usuarios"))
    )

def agregar_usuario(page: ft.Page):
    page.title = "Agregar Usuario"
    page.add(ft.Text("Aquí va el formulario de alta de usuario"))

def consultar_usuarios(page: ft.Page):
    page.title = "Consultar Usuarios"
    page.add(ft.Text("Aquí va la tabla de usuarios"))

ft.app(
    target=main,
    view=ft.WEB_BROWSER,
    routes={
        "/": main,
        "/principal": principal,
        "/agregar_usuario": agregar_usuario,
        "/consultar_usuarios": consultar_usuarios
    }
)
