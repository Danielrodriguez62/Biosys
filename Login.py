import flet as ft
from pyairtable import Table
from pyairtable.formulas import match
import principal as pr

# Configuración Airtable
AT_API_KEY = "patuASK11VeXlRg7q.95da8618bc32869c8ab41748d62e8ea5ce6fb29b4988ba5612f861a93061fc2b"
BASE_ID = "appO5xjRqKCWDWxyC"
TABLE_NAME = "usuario"

tabla = Table(AT_API_KEY, BASE_ID, TABLE_NAME)

def main(page: ft.Page):
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.title = "Inicio de sesión"
    page.window.width = 800
    page.window.height = 600

    txt_usuario = ft.TextField(label="Username/Correo", width=300)
    txt_contra = ft.TextField(label="Contraseña", password=True, width=300, can_reveal_password=True)
    mensaje = ft.Text(color="red")

    def ingresar(e: ft.ControlEvent):
        try:
            formula = match({"clave": txt_usuario.value, "contra": txt_contra.value})
            registro = tabla.first(formula=formula)
            if registro:
                mensaje.value = "Funciona!"
                page.clean()
                pr.main(page)
            else:
                mensaje.value = f"Usuario '{txt_usuario.value}' no encontrado."
            page.update()
        except Exception as ex:
            mensaje.value = f"Error de Airtable: {ex}"
            page.update()

    logo = ft.Icon("person", size=80, color="pink")
    txt_bienvenido = ft.Text("Bienvenid@", size=30)
    btn_login = ft.FilledButton(
        text="Iniciar sesión",
        icon=ft.Icons.LOGIN,
        width=250,
        color="white",
        bgcolor="pink",
        on_click=ingresar
    )

    page.add(logo, txt_bienvenido, txt_usuario, txt_contra, btn_login, mensaje)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)