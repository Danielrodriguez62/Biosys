import flet as ft
from pyairtable import Table

# --- Configuración Airtable ---
AT_API_KEY = "patuASK11VeXlRg7q.95da8618bc32869c8ab41748d62e8ea5ce6fb29b4988ba5612f861a93061fc2b"
BASE_ID = "appO5xjRqKCWDWxyC"
TABLE_NAME = "usuario"

tabla = Table(AT_API_KEY, BASE_ID, TABLE_NAME)

def main(page: ft.Page):
    def guardar_usuario(e: ft.ControlEvent):
        clave = txt_clave.value
        contra = txt_contra.value
        contra2 = txt_contra2.value
        nombre = txt_nombre.value

        # Validar campos
        if not clave:
            page.open(ft.SnackBar(ft.Text("Introduce tu clave de usuario"), bgcolor="yellow"))
            return
        if not contra:
            page.open(ft.SnackBar(ft.Text("Introduce tu contraseña"), bgcolor="red"))
            return
        if not contra2:
            page.open(ft.SnackBar(ft.Text("Confirma tu contraseña"), bgcolor="red"))
            return
        if contra != contra2:
            page.open(ft.SnackBar(ft.Text("Las contraseñas no coinciden"), bgcolor="red"))
            return
        if not nombre:
            page.open(ft.SnackBar(ft.Text("Introduce tu nombre"), bgcolor="red"))
            return

        # Guardar usuario en Airtable
        try:
            tabla.create({
                "clave": clave,
                "contra": contra,
                "nombre": nombre,
                "admin": chk_admin.value
            })
            page.open(ft.SnackBar(ft.Text("Usuario registrado correctamente"), bgcolor="blue", show_close_icon=True))
            txt_clave.value = ""
            txt_contra.value = ""
            txt_contra2.value = ""
            txt_nombre.value = ""
            chk_admin.value = False
            page.update()
        except Exception as error:
            page.open(ft.SnackBar(ft.Text(f"Error al registrar: {error}"), bgcolor="red", show_close_icon=True))

    # Configuración de la página
    page.title = "Altas"
    page.theme_mode = "light"
    page.window_width = 800
    page.window_height = 600
    page.appbar = ft.AppBar(
        title=ft.Text("Nuevo Usuario"),
        center_title=True,
        leading=ft.Icon("person_add"),
        color="white",
        bgcolor="blue"
    )

    # Componentes de entrada
    txt_clave = ft.TextField(label="Clave de usuario")
    txt_contra = ft.TextField(label="Contraseña", password=True)
    txt_contra2 = ft.TextField(label="Confirmar contraseña", password=True)
    txt_nombre = ft.TextField(label="Nombre completo")
    chk_admin = ft.Checkbox(label="¿Eres administrador?")

    btn_guardar = ft.FilledButton(
        text="Guardar",
        icon="save_as",
        bgcolor="green",
        on_click=guardar_usuario
    )
    btn_cancelar = ft.FilledButton(
        text="Cancelar",
        icon="cancel",
        bgcolor="red"
    )

    fila_botones = ft.Row(controls=[btn_guardar, btn_cancelar])
    page.add(txt_clave, txt_contra, txt_contra2, txt_nombre, chk_admin, fila_botones)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
