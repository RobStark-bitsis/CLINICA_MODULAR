import customtkinter as ctk
from tkcalendar import Calendar
from database import conectar_db

def obtener_lista_pacientes():
    """Trae todos los pacientes activos de MySQL"""
    lista_pacientes = []
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_paciente, nombre, apellido, dpi FROM pacientes ORDER BY nombre ASC")
            for (id_p, nom, ape, dpi) in cursor.fetchall():
                lista_pacientes.append({
                    "id": id_p,
                    "nombre_completo": f"{nom} {ape}",
                    "dpi": str(dpi),
                    "texto_combo": f"{nom} {ape} | DPI: {dpi}"
                })
        except Exception as e:
            print(f"Error al cargar pacientes: {e}")
        finally:
            conexion.close()
    return lista_pacientes

def crear_vista_citas(ventana, ir_a_dashboard):
    frame_citas = ctk.CTkScrollableFrame(ventana, fg_color="white", corner_radius=0)

    color_menta = "#7ED9A1"
    fuente_seccion = ("Arial", 16, "bold")
    fuente_label = ("Arial", 12, "bold")

    # Cargar datos desde la base de datos
    pacientes_datos = obtener_lista_pacientes()
    valores_pacientes = [p["texto_combo"] for p in pacientes_datos] if pacientes_datos else ["No hay pacientes registrados"]

    # Listas de datos fijos para los selectores de tiempo (Segmentados)
    lista_horas = [f"{i:02d}" for i in range(1, 13)]       # ["01", "02", ..., "12"]
    lista_minutos = [f"{i:02d}" for i in range(0, 60, 5)]  # ["00", "05", "10", ..., "55"] (Intervalos de 5 min)
    lista_periodo = ["AM", "PM"]

    # --- HEADER ---
    header = ctk.CTkFrame(frame_citas, fg_color=color_menta, height=40, corner_radius=0)
    header.pack(fill="x", pady=(10, 20))
    ctk.CTkLabel(header, text="  AGENDAR NUEVA CITA MÉDICA (SELECTORES DE TIEMPO AVANZADOS)", text_color="#1A1A1A", font=fuente_seccion).pack(side="left")

    grid_campos = ctk.CTkFrame(frame_citas, fg_color="white")
    grid_campos.pack(fill="x", padx=20)

    # 1. Buscador predictivo (Filtra por DPI o Nombre)
    ctk.CTkLabel(grid_campos, text="Buscar Paciente (Escriba Nombre o número de DPI)", text_color="black", font=fuente_label).grid(row=0, column=0, sticky="w", pady=(5,0))
    
    combo_paciente = ctk.CTkComboBox(grid_campos, values=valores_pacientes, width=500, fg_color="#F0F0F0", text_color="black", button_color=color_menta, button_hover_color="#5cb87c")
    combo_paciente.grid(row=1, column=0, pady=5, sticky="w")
    combo_paciente.set("")

    def filtrar_pacientes_dinamico(event):
        texto_buscado = combo_paciente.get().lower().strip()
        if not texto_buscado:
            combo_paciente.configure(values=valores_pacientes)
            return
        
        filtrados = [
            p["texto_combo"] for p in pacientes_datos 
            if texto_buscado in p["nombre_completo"].lower() or texto_buscado in p["dpi"]
        ]
        
        if filtrados:
            combo_paciente.configure(values=filtrados)
        else:
            combo_paciente.configure(values=["⚠️ Paciente no encontrado, verifique DPI o Nombre"])

    combo_paciente._entry.bind("<KeyRelease>", filtrar_pacientes_dinamico)

    # 2. Campo de fecha con selector de Calendario interactivo
    ctk.CTkLabel(grid_campos, text="Fecha de la Cita (DD/MM/AAAA)", text_color="black", font=fuente_label).grid(row=2, column=0, sticky="w", pady=(10,0))
    
    frame_fecha_sub = ctk.CTkFrame(grid_campos, fg_color="transparent")
    frame_fecha_sub.grid(row=3, column=0, pady=5, sticky="w")
    
    ent_fecha = ctk.CTkEntry(frame_fecha_sub, placeholder_text="dd/mm/yyyy", width=180, fg_color="#F0F0F0", text_color="black")
    ent_fecha.pack(side="left")

    def abrir_calendario_flotante():
        ventana_cal = ctk.CTkToplevel(ventana)
        ventana_cal.title("Seleccione la Fecha")
        ventana_cal.geometry("300x320")
        ventana_cal.grab_set()
        ventana_cal.resizable(False, False)
        ventana_cal.attributes("-topmost", True)

        cal = Calendar(ventana_cal, selectmode='day', date_pattern='dd/mm/yyyy', 
                       background="#005088", headersbackground="#7ED9A1", 
                       normalbackground="#F0F0F0", weekendbackground="#E0E0E0")
        cal.pack(pady=15, fill="both", expand=True, padx=10)

        def seleccionar_y_cerrar():
            ent_fecha.delete(0, "end")
            ent_fecha.insert(0, cal.get_date())
            ventana_cal.destroy()

        ctk.CTkButton(ventana_cal, text="Confirmar Fecha", fg_color="#28a745", command=seleccionar_y_cerrar).pack(pady=10)

    btn_cal = ctk.CTkButton(frame_fecha_sub, text="📅", width=40, fg_color=color_menta, hover_color="#5cb87c", text_color="black", command=abrir_calendario_flotante)
    btn_cal.pack(side="left", padx=10)

    # 🚀 3. NUEVA SOLUCIÓN VISUAL: Selector de Hora Segmentado (Igual al de tu imagen de referencia)
    ctk.CTkLabel(grid_campos, text="Hora de la Cita (Hora / Minutos / Periodo)", text_color="black", font=fuente_label).grid(row=4, column=0, sticky="w", pady=(10,0))
    
    frame_hora_segmentada = ctk.CTkFrame(grid_campos, fg_color="transparent")
    frame_hora_segmentada.grid(row=5, column=0, pady=5, sticky="w")

    # Menú Desplegable para la Hora (Ej: 08)
    combo_hr = ctk.CTkComboBox(frame_hora_segmentada, values=lista_horas, width=80, fg_color="#F0F0F0", text_color="black", button_color=color_menta)
    combo_hr.pack(side="left", padx=(0, 5))
    combo_hr.set("08") # Valor por defecto inicial

    # Texto intermedio separador ":"
    ctk.CTkLabel(frame_hora_segmentada, text=":", font=("Arial", 16, "bold"), text_color="black").pack(side="left", padx=2)

    # Menú Desplegable para los Minutos (Ej: 30)
    combo_min = ctk.CTkComboBox(frame_hora_segmentada, values=lista_minutos, width=80, fg_color="#F0F0F0", text_color="black", button_color=color_menta)
    combo_min.pack(side="left", padx=5)
    combo_min.set("00") # Valor por defecto inicial

    # Menú Desplegable para AM/PM
    combo_per = ctk.CTkComboBox(frame_hora_segmentada, values=lista_periodo, width=80, fg_color="#F0F0F0", text_color="black", button_color=color_menta)
    combo_per.pack(side="left", padx=5)
    combo_per.set("AM") # Valor por defecto inicial

    # Motivo de Consulta
    ctk.CTkLabel(grid_campos, text="Motivo o Especialidad de la Consulta", text_color="black", font=fuente_label).grid(row=6, column=0, sticky="w", pady=(10,0))
    ent_motivo = ctk.CTkEntry(grid_campos, placeholder_text="Ej: Consulta General, Pediatría, Control...", width=500, fg_color="#F0F0F0", text_color="black")
    ent_motivo.grid(row=7, column=0, pady=5, sticky="w")

    # --- BOTONES DE ACCIÓN ---
    frame_botones = ctk.CTkFrame(frame_citas, fg_color="white")
    frame_botones.pack(pady=40)

    def guardar_cita():
        seleccion = combo_paciente.get()
        fecha = ent_fecha.get().strip()
        motivo = ent_motivo.get().strip()

        # 🧠 Unificamos las tres cajitas en una sola cadena de texto limpia para la base de datos
        hora_final = f"{combo_hr.get()}:{combo_min.get()} {combo_per.get()}"

        if not seleccion or "⚠️" in seleccion or not fecha:
            print("⚠️ Asegúrese de seleccionar un paciente y una fecha válidos.")
            return

        nombre_paciente = seleccion.split(" | DPI:")[0]

        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO citas (paciente, fecha, hora, motivo) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nombre_paciente, fecha, hora_final, motivo))
                conexion.commit()
                print(f"¡Cita agendada para {nombre_paciente} a las {hora_final}! 📅")
                
                # Reseteamos los campos del formulario
                ent_fecha.delete(0, "end")
                combo_hr.set("08")
                combo_min.set("00")
                combo_per.set("AM")
                combo_paciente.set("")
                ent_motivo.delete(0, "end")
                ir_a_dashboard()
            except Exception as e:
                print(f"❌ Error en la base de datos MySQL: {e}")
            finally:
                conexion.close()

    ctk.CTkButton(frame_botones, text="AGENDAR CITA", fg_color="#28a745", hover_color="#218838", width=200, height=45, font=("Arial", 14, "bold"), command=guardar_cita).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="CANCELAR", fg_color="#dc3545", hover_color="#c82333", width=200, height=45, font=("Arial", 14, "bold"), command=ir_a_dashboard).pack(side="left", padx=10)

    return frame_citas