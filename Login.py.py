import flet as ft
import principal as pr

#funcion principal
def main(page: ft.Page):

    def ingresar(e: ft.ControlEvent):
        page.clean()
        pr.main(page)

    #Configuracion de la paguina
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.title = "Inicio de sesion"
    page.window.width = 800
    page.window.height = 600

    #Componentes de la pagina
    logo = ft.Icon("person", size=80, color="pink")
    txt_bienvenido = ft.Text("Bienvenid@", size=30)
    txt_usuario = ft.TextField(label="Username/Correo", width=300)
    txt_contra = ft.TextField(label="Contraseña", password=True, width=300, can_reveal_password=True )
    btn_login =  ft.FilledButton(
        text="Iniciar sesion",
        icon=ft.Icons.LOGIN ,
        width=250,
        color="white",
        bgcolor="pink",
        on_click=ingresar
        )

    page.add(logo,txt_bienvenido, txt_usuario, txt_contra, btn_login)

#Actualizar la pagina
    page.update()

#inicio de la aplicacion
if __name__== "__main__":
    ft.app(target=main,view=ft.AppView.WEB_BROWSER)
