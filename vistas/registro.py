import customtkinter as ctk
from database import conectar_db

def crear_vista_registro(ventana, ir_a_menu):
    # Usamos un ScrollableFrame por si la pantalla del usuario es pequeña, para que pueda bajar
    frame_pacientes = ctk.CTkScrollableFrame(ventana, fg_color="white", corner_radius=0)

    # Estilo de Colores
    color_menta = "#7ED9A1" # El verde menta de tu imagen
    color_texto_seccion = "#1A1A1A"
    fuente_seccion = ("Arial", 16, "bold")
    fuente_label = ("Arial", 12, "bold")

    # --- SECCIÓN 1: PERSONAL INFORMATION ---
    header_personal = ctk.CTkFrame(frame_pacientes, fg_color=color_menta, height=40, corner_radius=0)
    header_personal.pack(fill="x", pady=(10, 10))
    ctk.CTkLabel(header_personal, text="  PERSONAL INFORMATION", text_color=color_texto_seccion, font=fuente_seccion).pack(side="left")

    grid_personal = ctk.CTkFrame(frame_pacientes, fg_color="white")
    grid_personal.pack(fill="x", padx=20)

    # FILA 1: DPI y Full Name
    ctk.CTkLabel(grid_personal, text="DPI (Documento de Identidad)", text_color="black", font=fuente_label).grid(row=0, column=0, sticky="w", pady=(5,0))
    ctk.CTkLabel(grid_personal, text="Full Name", text_color="black", font=fuente_label).grid(row=0, column=1, sticky="w", pady=(5,0), padx=(20,0))
    
    ent_dpi = ctk.CTkEntry(grid_personal, placeholder_text="Ingrese el número de DPI", width=350, fg_color="#F0F0F0", text_color="black", border_color="#D1D1D1")
    ent_dpi.grid(row=1, column=0, pady=5, sticky="w")
    
    ent_nombre_completo = ctk.CTkEntry(grid_personal, placeholder_text="Nombre Y Apellido", width=350, fg_color="#F0F0F0", text_color="black", border_color="#D1D1D1")
    ent_nombre_completo.grid(row=1, column=1, pady=5, padx=(20,0), sticky="w")

    # Fila 2: Date of Birth y Gender
    ctk.CTkLabel(grid_personal, text="Date of birth (DD/MM/AAAA)", text_color="black", font=fuente_label).grid(row=2, column=0, sticky="w", pady=(10,0))
    ctk.CTkLabel(grid_personal, text="Gender", text_color="black", font=fuente_label).grid(row=2, column=1, sticky="w", pady=(10,0), padx=(20,0))
    
    ent_fecha_nac = ctk.CTkEntry(grid_personal, placeholder_text="dd/mm/yyyy", width=350, fg_color="#F0F0F0", text_color="black", border_color="#D1D1D1")
    ent_fecha_nac.grid(row=3, column=0, pady=5, sticky="w")
    
    frame_genero = ctk.CTkFrame(grid_personal, fg_color="transparent")
    frame_genero.grid(row=3, column=1, pady=5, padx=(20,0), sticky="w")
    var_genero = ctk.StringVar(value="Male")
    ctk.CTkRadioButton(frame_genero, text="Male", variable=var_genero, value="Male", text_color="black", hover_color=color_menta).pack(side="left", padx=5)
    ctk.CTkRadioButton(frame_genero, text="Female", variable=var_genero, value="Female", text_color="black", hover_color=color_menta).pack(side="left", padx=5)

    # Fila 3: Address y Phone Number
    ctk.CTkLabel(grid_personal, text="Address", text_color="black", font=fuente_label).grid(row=4, column=0, sticky="w", pady=(10,0))
    ctk.CTkLabel(grid_personal, text="Phone Number", text_color="black", font=fuente_label).grid(row=4, column=1, sticky="w", pady=(10,0), padx=(20,0))
    
    ent_direccion = ctk.CTkEntry(grid_personal, placeholder_text="Dirección de domicilio", width=350, fg_color="#F0F0F0", text_color="black", border_color="#D1D1D1")
    ent_direccion.grid(row=5, column=0, pady=5, sticky="w")
    
    ent_telefono = ctk.CTkEntry(grid_personal, placeholder_text="0000-0000", width=350, fg_color="#F0F0F0", text_color="black", border_color="#D1D1D1")
    ent_telefono.grid(row=5, column=1, pady=5, padx=(20,0), sticky="w")

    # Fila 4: Email solo
    ctk.CTkLabel(grid_personal, text="Email", text_color="black", font=fuente_label).grid(row=6, column=0, sticky="w", pady=(10,0))
    ent_email = ctk.CTkEntry(grid_personal, placeholder_text="ejemplo@correo.com", width=350, fg_color="#F0F0F0", text_color="black", border_color="#D1D1D1")
    ent_email.grid(row=7, column=0, pady=5, sticky="w")

    # --- SECCIÓN 2: EMERGENCY CONTACT ---
    header_emergencia = ctk.CTkFrame(frame_pacientes, fg_color=color_menta, height=40, corner_radius=0)
    header_emergencia.pack(fill="x", pady=(20, 10))
    ctk.CTkLabel(header_emergencia, text="  EMERGENCY CONTACT DETAILS", text_color=color_texto_seccion, font=fuente_seccion).pack(side="left")

    grid_emergencia = ctk.CTkFrame(frame_pacientes, fg_color="white")
    grid_emergencia.pack(fill="x", padx=20)

    ctk.CTkLabel(grid_emergencia, text="Name", text_color="black", font=fuente_label).grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(grid_emergencia, text="Relationship", text_color="black", font=fuente_label).grid(row=0, column=1, sticky="w", padx=(20,0))
    ctk.CTkLabel(grid_emergencia, text="Phone Number", text_color="black", font=fuente_label).grid(row=0, column=2, sticky="w", padx=(20,0))

    ent_emer_nombre = ctk.CTkEntry(grid_emergencia, width=230, fg_color="#F0F0F0", text_color="black")
    ent_emer_nombre.grid(row=1, column=0, pady=5)
    ent_emer_relacion = ctk.CTkEntry(grid_emergencia, width=230, fg_color="#F0F0F0", text_color="black")
    ent_emer_relacion.grid(row=1, column=1, pady=5, padx=(20,0))
    ent_emer_tel = ctk.CTkEntry(grid_emergencia, width=230, fg_color="#F0F0F0", text_color="black")
    ent_emer_tel.grid(row=1, column=2, pady=5, padx=(20,0))

    # --- SECCIÓN EXTRA: MEDICAL INFO ---
    header_medico = ctk.CTkFrame(frame_pacientes, fg_color=color_menta, height=40, corner_radius=0)
    header_medico.pack(fill="x", pady=(20, 10))
    ctk.CTkLabel(header_medico, text="  MEDICAL INFORMATION (EXTRA)", text_color=color_texto_seccion, font=fuente_seccion).pack(side="left")

    grid_medico = ctk.CTkFrame(frame_pacientes, fg_color="white")
    grid_medico.pack(fill="x", padx=20)

    ctk.CTkLabel(grid_medico, text="Enfermedades Pre-existentes", text_color="black", font=fuente_label).grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(grid_medico, text="Alergias Conocidas", text_color="black", font=fuente_label).grid(row=0, column=1, sticky="w", padx=(20,0))

    txt_enfermedades = ctk.CTkTextbox(grid_medico, width=350, height=70, fg_color="#F0F0F0", text_color="black", border_width=1)
    txt_enfermedades.grid(row=1, column=0, pady=5, sticky="w")
    txt_alergias = ctk.CTkTextbox(grid_medico, width=350, height=70, fg_color="#F0F0F0", text_color="black", border_width=1)
    txt_alergias.grid(row=1, column=1, pady=5, padx=(20,0), sticky="w")

    # --- BOTONES DE ACCIÓN ---
    frame_botones = ctk.CTkFrame(frame_pacientes, fg_color="white")
    frame_botones.pack(pady=30)

    # 🧼 Función interna para dejar el formulario vacío
    def limpiar_formulario():
        ent_dpi.delete(0, "end")
        ent_nombre_completo.delete(0, "end")
        ent_fecha_nac.delete(0, "end")
        ent_direccion.delete(0, "end")
        ent_telefono.delete(0, "end")
        ent_email.delete(0, "end")
        ent_emer_nombre.delete(0, "end")
        ent_emer_relacion.delete(0, "end")
        ent_emer_tel.delete(0, "end")
        txt_enfermedades.delete("1.0", "end")
        txt_alergias.delete("1.0", "end")
        var_genero.set("Male")

    def guardar_datos():
        nombre_completo = ent_nombre_completo.get().strip()
        dpi = ent_dpi.get().strip()
        telefono = ent_telefono.get().strip()

        if not dpi or not nombre_completo or not telefono:
            print("⚠️ El DPI, Full Name y Teléfono son campos obligatorios.")
            return

        partes = nombre_completo.split(" ", 1)
        nombre = partes[0]
        apellido = partes[1] if len(partes) > 1 else " "

        datos = (
            dpi, nombre, apellido, ent_fecha_nac.get().strip(), 
            var_genero.get(), ent_direccion.get().strip(), telefono, 
            ent_email.get().strip(), ent_emer_nombre.get().strip(), ent_emer_relacion.get().strip(), 
            ent_emer_tel.get().strip(), txt_enfermedades.get("1.0", "end").strip(), txt_alergias.get("1.0", "end").strip()
        )

        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO pacientes 
                         (dpi, nombre, apellido, fecha_nacimiento, genero, direccion, telefono, email, emer_nombre, emer_relacion, emer_telefono, enfermedades, alergias) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, datos)
                conexion.commit()
                print("¡Paciente registrado exitosamente! 🩺")
                
                # 🧼 LUEGO DE GUARDAR: Limpiamos los campos y regresamos
                limpiar_formulario()
                ir_a_menu()
            except Exception as e:
                print(f"❌ Error al guardar en MySQL: {e}")
            finally:
                conexion.close()

    def cancelar_registro():
        limpiar_formulario() # También limpia si el usuario decide cancelar sin guardar
        ir_a_menu()

    ctk.CTkButton(frame_botones, text="REGISTRAR PACIENTE", fg_color="#28a745", hover_color="#218838", width=250, height=45, font=("Arial", 14, "bold"), command=guardar_datos).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="CANCELAR", fg_color="#dc3545", hover_color="#c82333", width=250, height=45, font=("Arial", 14, "bold"), command=cancelar_registro).pack(side="left", padx=10)

    return frame_pacientes