import flet as ft
import requests

# Configuración Airtable
api_key = "pathV21BLd8k98N4X.08ad9943ce9829f9142770440ceddf92f24ece14703795fbb265149dd7a2d2f5"
base_id = "appO5xjRqKCWDWxyC"
table_usuarios = "usuarios"
table_bioenergia = "bioenergia"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Conexión
def probar_conexion():
    url = f"https://api.airtable.com/v0/{base_id}/{table_usuarios}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

def agregar_usuario(data):
    url = f"https://api.airtable.com/v0/{base_id}/{table_usuarios}"
    response = requests.post(url, headers=headers, json={"fields": data})
    return response.status_code in [200, 201]

def agregar_bioenergia(data):
    url = f"https://api.airtable.com/v0/{base_id}/{table_bioenergia}"
    response = requests.post(url, headers=headers, json={"fields": data})
    return response.status_code in [200, 201]

def consultar_usuarios():
    url = f"https://api.airtable.com/v0/{base_id}/{table_usuarios}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("records", [])
    return []

def consultar_bioenergias():
    url = f"https://api.airtable.com/v0/{base_id}/{table_bioenergia}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("records", [])
    return []

def validar_login(usuario, contrasena):
    usuarios = consultar_usuarios()
    for u in usuarios:
        datos = u["fields"]
        if datos.get("Usuario") == usuario and datos.get("Contraseña") == contrasena:
            return datos.get("Admin", "No")
    return None

# Interfaz
def main(page: ft.Page):
    page.title = "🌱 Sistema de Bioenergía - Tabasco"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.GREEN_50
    page.padding = 20

    primary_color = "#2E7D32"
    accent_color = "#00796B"
    warning_color = "#FF8F00"
    error_color = "#C62828"
    success_color = "#388E3C"

    def crear_boton(texto, icono, color, accion=None, ancho=300):
        return ft.FilledTonalButton(
            text=texto,
            icon=icono,
            width=ancho,
            height=45,
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=accion
        )

    def crear_campo_texto(label, icono=None, password=False, ancho=300):
        return ft.TextField(
            label=label,
            password=password,
            can_reveal_password=password,
            border_radius=10,
            border_color=primary_color,
            focused_border_color=accent_color,
            prefix_icon=icono,
            width=ancho,
            text_size=14
        )

    def mostrar_snackbar(mensaje, tipo="info"):
        color_map = {
            "error": error_color,
            "warning": warning_color,
            "success": success_color,
            "info": accent_color
        }
        color = color_map.get(tipo, accent_color)
        page.snack_bar = ft.SnackBar(
            ft.Text(mensaje, color=ft.colors.WHITE),
            bgcolor=color,
            behavior=ft.SnackBarBehavior.FLOATING,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
        page.snack_bar.open = True
        page.update()

    # Login
    def mostrar_login():
        page.clean()

        titulo = ft.Text(
            "Bienvenido al Sistema",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=primary_color
        )
        subtitulo = ft.Text(
            "Gestión de Bioenergías de Tabasco",
            size=14,
            color=ft.colors.GREY_600
        )
        campo_usuario = crear_campo_texto("Usuario", ft.icons.PERSON)
        campo_contrasena = crear_campo_texto("Contraseña", ft.icons.LOCK, True)
        boton_login = crear_boton("Iniciar sesión", ft.icons.LOGIN, primary_color,
                                 lambda e: procesar_login(campo_usuario.value, campo_contrasena.value))

        def on_hover(e):
            e.control.bgcolor = accent_color if e.data == "true" else primary_color
            e.control.update()
        boton_login.on_hover = on_hover

        card_login = ft.Card(
            elevation=15,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([ft.Icon(ft.icons.ECO, size=40, color=primary_color)],
                               alignment=ft.MainAxisAlignment.CENTER),
                        titulo,
                        subtitulo,
                        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                        campo_usuario,
                        campo_contrasena,
                        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                        boton_login,
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=30,
                width=400,
                border_radius=15,
                bgcolor=ft.colors.WHITE,
            )
        )

        page.add(
            ft.Stack(
                [
                    ft.Container(
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=["#E8F5E9", "#C8E6C9"]
                        ),
                        expand=True
                    ),
                    ft.Row([card_login], alignment=ft.MainAxisAlignment.CENTER)
                ],
                expand=True
            )
        )

    # Menu principal
    def mostrar_menu(admin_status):
        page.clean()
        es_admin = str(admin_status).lower() in ["sí", "si", "yes", "true", "1"]

        botones = []

        if es_admin:
            botones.append(crear_boton("Agregar nuevo usuario", ft.icons.PERSON_ADD, primary_color, lambda e: mostrar_agregar_usuario()))
        botones.extend([
            crear_boton("Agregar bioenergía", ft.icons.GRASS, accent_color, lambda e: mostrar_agregar_bioenergia()),
            crear_boton("Consultar usuarios", ft.icons.GROUP, primary_color, lambda e: mostrar_consultar_usuarios()),
            crear_boton("Consultar bioenergías", ft.icons.DATABASE, accent_color, lambda e: mostrar_consultar_bioenergias()),
            crear_boton("Cerrar sesión", ft.icons.LOGOUT, error_color, lambda e: mostrar_login()),
        ])

        page.add(
            ft.Column(
                [
                    ft.Text("Menú Principal", size=24, weight=ft.FontWeight.BOLD, color=primary_color),
                    ft.Divider(height=20),
                    ft.Column(botones, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        )

    # Agregar Usuario
    def mostrar_agregar_usuario():
        page.clean()
        campo_usuario = crear_campo_texto("Usuario", ft.icons.PERSON)
        campo_contrasena = crear_campo_texto("Contraseña", ft.icons.LOCK, True)
        campo_nombre = crear_campo_texto("Nombre", ft.icons.BADGE)
        campo_admin = ft.Checkbox(label="Administrador", value=False)

        boton_guardar = crear_boton("Guardar usuario", ft.icons.SAVE, primary_color)
        boton_cancelar = crear_boton("Cancelar", ft.icons.CANCEL, warning_color)

        def guardar_usuario(e):
            if not campo_usuario.value or not campo_contrasena.value or not campo_nombre.value:
                mostrar_snackbar("Por favor, complete todos los campos", "warning")
                return
            data = {
                "Usuario": campo_usuario.value.strip(),
                "Contraseña": campo_contrasena.value.strip(),
                "Nombre": campo_nombre.value.strip(),
                "Admin": "Sí" if campo_admin.value else "No"
            }
            if agregar_usuario(data):
                mostrar_snackbar("Usuario agregado exitosamente", "success")
                mostrar_menu("Sí")
            else:
                mostrar_snackbar("Error al agregar usuario", "error")

        def cancelar(e):
            mostrar_menu("Sí")

        boton_guardar.on_click = guardar_usuario
        boton_cancelar.on_click = cancelar

        page.add(
            ft.Column(
                [
                    ft.Text("Agregar nuevo usuario", size=24, weight=ft.FontWeight.BOLD, color=primary_color),
                    campo_usuario,
                    campo_contrasena,
                    campo_nombre,
                    campo_admin,
                    ft.Row([boton_guardar, boton_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    # Agregar Bioenergia
    def mostrar_agregar_bioenergia():
        page.clean()
        campo_cultivo = crear_campo_texto("Cultivo")
        campo_parte = crear_campo_texto("Parte")
        campo_cantidad = crear_campo_texto("Cantidad (Ton)")
        campo_humedad = crear_campo_texto("Humedad (%)")
        campo_area = crear_campo_texto("Área cultivada")
        campo_contenido = crear_campo_texto("Contenido energético")
        campo_municipio = crear_campo_texto("Municipio")
        campo_latitud = crear_campo_texto("Latitud")
        campo_longitud = crear_campo_texto("Longitud")

        boton_guardar = crear_boton("Guardar bioenergía", ft.icons.SAVE, accent_color)
        boton_cancelar = crear_boton("Cancelar", ft.icons.CANCEL, warning_color)

        def guardar_bioenergia(e):
            if (not campo_cultivo.value or not campo_parte.value or not campo_cantidad.value or
                not campo_humedad.value or not campo_area.value or not campo_contenido.value or
                not campo_municipio.value or not campo_latitud.value or not campo_longitud.value):
                mostrar_snackbar("Complete todos los campos", "warning")
                return
            data = {
                "Cultivo": campo_cultivo.value.strip(),
                "Parte": campo_parte.value.strip(),
                "Cantidad (Ton)": campo_cantidad.value.strip(),
                "Humedad (%)": campo_humedad.value.strip(),
                "Área cultivada": campo_area.value.strip(),
                "Contenido energético": campo_contenido.value.strip(),
                "Municipio": campo_municipio.value.strip(),
                "Latitud": campo_latitud.value.strip(),
                "Longitud": campo_longitud.value.strip(),
            }
            if agregar_bioenergia(data):
                mostrar_snackbar("Bioenergía agregada exitosamente", "success")
                mostrar_menu("No")
            else:
                mostrar_snackbar("Error al agregar bioenergía", "error")

        def cancelar(e):
            mostrar_menu("No")

        boton_guardar.on_click = guardar_bioenergia
        boton_cancelar.on_click = cancelar

        page.add(
            ft.Column(
                [
                    ft.Text("Agregar Bioenergía", size=24, weight=ft.FontWeight.BOLD, color=primary_color),
                    campo_cultivo,
                    campo_parte,
                    campo_cantidad,
                    campo_humedad,
                    campo_area,
                    campo_contenido,
                    campo_municipio,
                    campo_latitud,
                    campo_longitud,
                    ft.Row([boton_guardar, boton_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    #Consultar usuarios
    def mostrar_consultar_usuarios():
        page.clean()
        registros = consultar_usuarios()

        filas = []
        for r in registros:
            f = r.get("fields", {})
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f.get("Usuario", ""))),
                        ft.DataCell(ft.Text(f.get("Nombre", ""))),
                        ft.DataCell(ft.Text(str(f.get("Admin", "")))),
                    ]
                )
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Usuario")),
                ft.DataColumn(label=ft.Text("Nombre")),
                ft.DataColumn(label=ft.Text("Admin")),
            ],
            rows=filas,
            column_spacing=20,
            heading_row_color=ft.colors.GREEN_100,
        )

        boton_volver = crear_boton("Volver al Menú", ft.icons.ARROW_BACK, warning_color, lambda e: mostrar_menu("No"))

        page.add(
            ft.Column(
                [
                    ft.Text("Usuarios Registrados", size=24, weight=ft.FontWeight.BOLD, color=primary_color),
                    tabla,
                    boton_volver,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    #Consultar Bioenergias
    def mostrar_consultar_bioenergias():
        page.clean()
        registros = consultar_bioenergias()

        filas = []
        for r in registros:
            f = r.get("fields", {})
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f.get("Cultivo", ""))),
                        ft.DataCell(ft.Text(f.get("Parte", ""))),
                        ft.DataCell(ft.Text(str(f.get("Cantidad (Ton)", "")))),
                        ft.DataCell(ft.Text(str(f.get("Humedad (%)", "")))),
                        ft.DataCell(ft.Text(str(f.get("Área cultivada", "")))),
                        ft.DataCell(ft.Text(str(f.get("Contenido energético", "")))),
                        ft.DataCell(ft.Text(f.get("Municipio", ""))),
                        ft.DataCell(ft.Text(str(f.get("Latitud", "")))),
                        ft.DataCell(ft.Text(str(f.get("Longitud", "")))),
                    ]
                )
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Cultivo")),
                ft.DataColumn(label=ft.Text("Parte")),
                ft.DataColumn(label=ft.Text("Cantidad (Ton)")),
                ft.DataColumn(label=ft.Text("Humedad (%)")),
                ft.DataColumn(label=ft.Text("Área cultivada")),
                ft.DataColumn(label=ft.Text("Contenido energético")),
                ft.DataColumn(label=ft.Text("Municipio")),
                ft.DataColumn(label=ft.Text("Latitud")),
                ft.DataColumn(label=ft.Text("Longitud")),
            ],
            rows=filas,
            column_spacing=15,
            heading_row_color=ft.colors.GREEN_100,
        )

        boton_volver = crear_boton("Volver al Menú", ft.icons.ARROW_BACK, warning_color, lambda e: mostrar_menu("No"))

        page.add(
            ft.Column(
                [
                    ft.Text("Bioenergías Registradas", size=24, weight=ft.FontWeight.BOLD, color=primary_color),
                    tabla,
                    boton_volver,
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    # Procesar Login
    def procesar_login(usuario, contrasena):
        if not usuario or not contrasena:
            mostrar_snackbar("❌ Ingrese usuario y contraseña", "error")
            return
        admin_status = validar_login(usuario, contrasena)
        if admin_status:
            mostrar_snackbar(f"✅ Bienvenido, {usuario}", "success")
            mostrar_menu(admin_status)
        else:
            mostrar_snackbar("❌ Usuario o contraseña incorrectos", "error")

    # Inicio
    if probar_conexion():
        mostrar_login()
    else:
        page.add(ft.Text("❌ Error de conexión con Airtable", color=error_color))


if __name__ == "__main__":
    ft.app(target=main)