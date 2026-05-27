import customtkinter as ctk
from vistas.menu import crear_vista_menu
from vistas.registro import crear_vista_registro
from vistas.listado import crear_vista_listado
from vistas.dashboard import crear_vista_dashboard
from vistas.citas import crear_vista_citas  # 👈 Importamos el nuevo módulo

ctk.set_appearance_mode("dark")
ventana = ctk.CTk()
ventana.title("Sistema Médico Profesional")
ventana.after(0, lambda: ventana.state("zoomed"))

contenedor_derecho = ctk.CTkFrame(ventana, fg_color="#0f172a", corner_radius=0)
contenedor_derecho.grid(row=0, column=1, sticky="nsew")

ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(0, weight=1)

def mostrar_pantalla(pantalla_funcion):
    for child in contenedor_derecho.winfo_children():
        child.destroy()
    nueva_pantalla = pantalla_funcion(contenedor_derecho)
    nueva_pantalla.pack(fill="both", expand=True)

# Diccionario de navegación actualizado con el módulo de citas
navegacion = {
    'dashboard': lambda: mostrar_pantalla(crear_vista_dashboard),
    'registro': lambda: mostrar_pantalla(lambda master: crear_vista_registro(master, lambda: mostrar_pantalla(crear_vista_dashboard))),
    'listado': lambda: mostrar_pantalla(lambda master: crear_vista_listado(master, lambda: mostrar_pantalla(crear_vista_dashboard))[0]),
    'citas': lambda: mostrar_pantalla(lambda master: crear_vista_citas(master, lambda: mostrar_pantalla(crear_vista_dashboard))) # 👈 Enlace del módulo citas
}

barra_lateral = crear_vista_menu(ventana, navegacion)
barra_lateral.grid(row=0, column=0, sticky="nsew")

# Arrancar la aplicación directo en el Dashboard renovado
mostrar_pantalla(crear_vista_dashboard)

ventana.mainloop()