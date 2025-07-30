import flet as ft
import Interfaz_RegiDatos as IRD
import ConsultasUsu as CS
import alta_usuario as AU

def main (page: ft.Page):
    #Configuración de la pagina
    page.theme_mode = "light" 
    page.horizontal_alignment = "center" 
    page.title = "Menú Principal" 
    page.window.width = 800 
    page.window.height = 600 
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
    }
    #Funciones para abrir las otras paginas
    def mostrar_registrodatos(e: ft.ControlEvent):
        page.clean()
        IRD.main(page)
    def mostrar_consultasUsu (e: ft.ControlEvent):
        page.clean()
        CS.main(page)
    def mostrar_altaUsu(e: ft.ControlEvent):
        page.clean()
        AU.main(page)
    #Componentes de la pagina
    page.appbar = ft.AppBar (
        title= ft.Text ("Sistema de Gestión de Bionergías",font_family="Kanit",size=30),
        center_title=True,
        leading= ft.Icon ("ENERGY_SAVINGS_LEAF"),
        color = "black",
        bgcolor= ft.Colors.RED_100,
    )

    
    btn_registro = ft.ElevatedButton ("Registro de bioenergias", on_click =mostrar_registrodatos )
    btn_consulta = ft.ElevatedButton ("Consulta de usuarios", on_click=mostrar_consultasUsu)
    btn_alta = ft.ElevatedButton ("Registro de usuarios (altas)", on_click=mostrar_altaUsu)


    #Añadir a la pagina y actualizar
    page.add(btn_registro,btn_consulta,btn_alta) 
    page.update() 

if __name__ == "__main__":
    ft.app(target=main)