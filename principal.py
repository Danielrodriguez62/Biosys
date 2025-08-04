import flet as ft 
import Interfaz_RegiDatos as IRD
import ConsultasUsu as CS
import alta_usuario as AU

def main(page: ft.Page):
    # Configuración de la página
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.title = "Menú Principal"
    page.window.width = 800
    page.window.height = 600
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
    }

    # Funciones para abrir las otras páginas
    def mostrar_registrodatos(e: ft.ControlEvent):
        page.clean()
        IRD.main(page)

    def mostrar_consultasUsu(e: ft.ControlEvent):
        page.clean()
        CS.main(page)

    def mostrar_altaUsu(e: ft.ControlEvent):
        page.clean()
        AU.main(page)

    # AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("Sistema de Gestión de Bioenergías", font_family="Kanit", size=30),
        center_title=True,
        leading=ft.Icon("ENERGY_SAVINGS_LEAF"),
        color="black",
        bgcolor=ft.Colors.RED_100,
    )

    # Botones requeridos por el examen
    btn_registro = ft.ElevatedButton("Registro de bioenergías", on_click=mostrar_registrodatos)
    btn_alta = ft.ElevatedButton("Agregar nuevo usuario", on_click=mostrar_altaUsu)  # renombrado
    btn_consulta = ft.ElevatedButton("Consultar usuarios", on_click=mostrar_consultasUsu)  # renombrado

    # Añadir a la página y actualizar
    page.add(btn_registro, btn_alta, btn_consulta)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
