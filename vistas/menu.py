import customtkinter as ctk

def crear_vista_menu(ventana, funciones_navegacion):
    sidebar = ctk.CTkFrame(ventana, width=220, fg_color="#005088", corner_radius=0)
    
    lbl_logo = ctk.CTkLabel(sidebar, text="CLÍNICA\nSANTA SALUD", font=("Arial", 20, "bold"), text_color="#7ED9A1")
    lbl_logo.pack(pady=(30, 40))

    def crear_boton_menu(texto, icono, comando):
        btn = ctk.CTkButton(sidebar, text=f" {icono}  {texto}", 
                            anchor="w", 
                            fg_color="transparent", 
                            hover_color="#334155",
                            font=("Arial", 14),
                            height=45,
                            command=comando)
        btn.pack(fill="x", padx=10, pady=2)
        return btn

    crear_boton_menu("Dashboard", "📊", funciones_navegacion['dashboard'])
    crear_boton_menu("Registrar Paciente", "👤", funciones_navegacion['registro'])
    crear_boton_menu("Listado General", "📋", funciones_navegacion['listado'])
    crear_boton_menu("Programar Cita", "📅", funciones_navegacion['citas']) # 👈 Reemplazo de Facturación realizado con éxito
    crear_boton_menu("Historial Clínico", "📂", lambda: print("Historial"))
    crear_boton_menu("Recetas Médicas", "💊", lambda: print("Recetas"))
    
    btn_salir = ctk.CTkButton(sidebar, text=" 🚪  Cerrar Sesión", fg_color="#721c24", hover_color="#af2d2d", command=ventana.quit)
    btn_salir.pack(side="bottom", fill="x", padx=20, pady=30)

    return sidebar