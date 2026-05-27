import customtkinter as ctk
from tkinter import ttk
import datetime
from weasyprint import HTML
import os
from database import conectar_db

def crear_vista_listado(ventana, ir_a_menu):
    frame_lista = ctk.CTkFrame(ventana)
    id_paciente_seleccionado = [None] # Mantiene el ID del paciente en memoria
    nombre_paciente_global = [""]      # Mantiene el nombre del paciente en memoria para el PDF

    # =====================================================
    # CONTENEDOR 1: LA TABLA PRINCIPAL Y EL BUSCADOR
    # =====================================================
    frame_contenido_tabla = ctk.CTkFrame(frame_lista, fg_color="transparent")
    frame_contenido_tabla.pack(fill="both", expand=True)

    titulo_lista = ctk.CTkLabel(frame_contenido_tabla, text="LISTADO DE PACIENTES", font=("Arial", 24, "bold"))
    titulo_lista.pack(pady=20)

    frame_buscador = ctk.CTkFrame(frame_contenido_tabla, fg_color="transparent")
    frame_buscador.pack(pady=5)

    entrada_busqueda = ctk.CTkEntry(frame_buscador, placeholder_text="Buscar por DPI, Nombre o Apellido...", width=280)
    entrada_busqueda.pack(side="left", padx=5)

    columnas = ("ID", "DPI", "Nombre", "Apellido", "Ultima Cita")
    tabla_pacientes = ttk.Treeview(frame_contenido_tabla, columns=columnas, show="headings", height=12)
    
    tabla_pacientes.heading("ID", text="ID")
    tabla_pacientes.heading("DPI", text="DPI")
    tabla_pacientes.heading("Nombre", text="Nombre")
    tabla_pacientes.heading("Apellido", text="Apellido")
    tabla_pacientes.heading("Ultima Cita", text="Última Cita (Fecha y Hora)")

    tabla_pacientes.column("ID", width=50, anchor="center")
    tabla_pacientes.column("DPI", width=130, anchor="center")
    tabla_pacientes.column("Nombre", width=200)
    tabla_pacientes.column("Apellido", width=200)
    tabla_pacientes.column("Ultima Cita", width=220, anchor="center")
    tabla_pacientes.pack(pady=15)

    # =====================================================
    # CONTENEDOR 2: EL FORMULARIO DE CONSULTA MÉDICA
    # =====================================================
    sub_frame_consulta = ctk.CTkFrame(frame_lista, fg_color=frame_lista.cget("fg_color")) 

    label_atendiendo = ctk.CTkLabel(sub_frame_consulta, text="Atendiendo a: ", font=("Arial", 18, "bold"))
    label_atendiendo.pack(pady=10)

    ctk.CTkLabel(sub_frame_consulta, text="Síntomas y Motivo de Consulta:").pack()
    entrada_sintomas = ctk.CTkTextbox(sub_frame_consulta, width=600, height=80)
    entrada_sintomas.pack(pady=3)

    ctk.CTkLabel(sub_frame_consulta, text="Diagnóstico Médico:").pack()
    entrada_diagnostico = ctk.CTkTextbox(sub_frame_consulta, width=600, height=80)
    entrada_diagnostico.pack(pady=3)

    ctk.CTkLabel(sub_frame_consulta, text="Medicamentos Recetados (Receta):").pack()
    entrada_receta = ctk.CTkTextbox(sub_frame_consulta, width=600, height=80)
    entrada_receta.pack(pady=3)

    # =====================================================
    # CONTENEDOR 3: PANTALLA DE HISTORIAL / BITÁCORA CLÍNICA 📅
    # =====================================================
    sub_frame_historial = ctk.CTkFrame(frame_lista, fg_color=frame_lista.cget("fg_color"))

    label_historial_titulo = ctk.CTkLabel(sub_frame_historial, text="HISTORIAL CLÍNICO: ", font=("Arial", 20, "bold"))
    label_historial_titulo.pack(pady=10)

    # RE-DISEÑO TOTAL: SECCIÓN DE FILTROS POR CUADRÍCULA (GRID) PARA EVITAR QUE SE OCULTEN
    frame_filtros = ctk.CTkFrame(sub_frame_historial, fg_color="transparent")
    frame_filtros.pack(pady=10)

    label_desde = ctk.CTkLabel(frame_filtros, text="Desde (AAAA-MM-DD):", font=("Arial", 12))
    label_desde.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    
    entrada_fecha_inicio = ctk.CTkEntry(frame_filtros, placeholder_text="Ej: 2026-05-01", width=130)
    entrada_fecha_inicio.grid(row=0, column=1, padx=5, pady=5)

    label_hasta = ctk.CTkLabel(frame_filtros, text="Hasta (AAAA-MM-DD):", font=("Arial", 12))
    label_hasta.grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    entrada_fecha_fin = ctk.CTkEntry(frame_filtros, placeholder_text="Ej: 2026-05-26", width=130)
    entrada_fecha_fin.grid(row=0, column=3, padx=5, pady=5)

    # Tabla de Historial Clínico
    columnas_historial = ("Fecha", "Motivo", "Diagnostico", "Medicamentos")
    tabla_historial = ttk.Treeview(sub_frame_historial, columns=columnas_historial, show="headings", height=10)
    
    tabla_historial.heading("Fecha", text="Fecha y Hora de la Cita")
    tabla_historial.heading("Motivo", text="Síntomas / Motivo")
    tabla_historial.heading("Diagnostico", text="Diagnóstico Médico")
    tabla_historial.heading("Medicamentos", text="Tratamiento / Receta")

    tabla_historial.column("Fecha", width=180, anchor="center")
    tabla_historial.column("Motivo", width=250)
    tabla_historial.column("Diagnostico", width=250)
    tabla_historial.column("Medicamentos", width=250)
    tabla_historial.pack(pady=10, fill="x", padx=20)

    # -----------------------------------------------------
    # LÓGICA DE DATOS Y FUNCIONES
    # -----------------------------------------------------
    def cargar_datos():
        for fila in tabla_pacientes.get_children():
            tabla_pacientes.delete(fila)
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            sql = """SELECT p.id_paciente, p.dpi, p.nombre, p.apellido, MAX(h.fecha_visita) AS ultima_cita
                     FROM pacientes p LEFT JOIN historial_visitas h ON p.id_paciente = h.id_paciente
                     GROUP BY p.id_paciente"""
            cursor.execute(sql)
            for registro in cursor.fetchall():
                valores = list(registro)
                if valores[4] is None: valores[4] = "Sin citas registradas"
                tabla_pacientes.insert("", "end", values=valores)
            conexion.close()

    def ejecutar_busqueda():
        texto = entrada_busqueda.get().lower().strip()
        if not texto: return
        for fila in tabla_pacientes.get_children(): tabla_pacientes.delete(fila)
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            sql = """SELECT p.id_paciente, p.dpi, p.nombre, p.apellido, MAX(h.fecha_visita) AS ultima_cita
                     FROM pacientes p LEFT JOIN historial_visitas h ON p.id_paciente = h.id_paciente
                     WHERE LOWER(p.dpi) LIKE %s OR LOWER(p.nombre) LIKE %s OR LOWER(p.apellido) LIKE %s
                     GROUP BY p.id_paciente"""
            cursor.execute(sql, (f"%{texto}%", f"%{texto}%", f"%{texto}%"))
            for registro in cursor.fetchall():
                valores = list(registro)
                if valores[4] is None: valores[4] = "Sin citas registradas"
                tabla_pacientes.insert("", "end", values=valores)
            conexion.close()
        entrada_busqueda.delete(0, "end")

    def generar_pdf(id_paciente, nombre, sintomas, diagnostico, receta):
        fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
        html_code = f"""
        <html><head><meta charset='UTF-8'><style>
            @page {{ size: letter; margin: 20mm 15mm; }}
            body {{ font-family: Arial, sans-serif; color: #2d3748; line-height: 1.6; }}
            .header {{ border-bottom: 3px solid #3182ce; padding-bottom: 10px; margin-bottom: 20px; }}
            .title {{ font-size: 24pt; font-weight: bold; color: #2b6cb0; text-transform: uppercase; }}
            .table-info {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; background: #f7fafc; border: 1px solid #e2e8f0; }}
            .table-info td {{ padding: 10px; border: 1px solid #e2e8f0; }}
            .section-title {{ font-size: 13pt; font-weight: bold; color: #2c5282; border-left: 4px solid #3182ce; padding-left: 8px; margin-top: 20px; text-transform: uppercase; }}
            .content-box {{ background: #ffffff; border: 1px solid #e2e8f0; padding: 12px; min-height: 60px; border-radius: 4px; white-space: pre-line; }}
            .receta-box {{ border: 1px dashed #4299e1; background-color: #ebf8ff; }}
            .signature {{ margin-top: 50px; text-align: center; }}
            .line {{ width: 220px; border-bottom: 1px solid #a0aec0; margin: 0 auto 5px auto; }}
        </style></head><body>
            <div class='header'><h1 class='title'>SISTEMA CLÍNICO MÉDICO</h1><p>Control de Consultas y Prescripciones</p></div>
            <table class='table-info'>
                <tr><td><b>Paciente:</b></td><td>{nombre}</td><td><b>Fecha:</b></td><td>{fecha_actual}</td></tr>
                <tr><td><b>ID Registro:</b></td><td>{id_paciente}</td><td><b>Documento:</b></td><td>Historial y Receta</td></tr>
            </table>
            <div class='section-title'>Diagnóstico Médico</div><div class='content-box'>{diagnostico}</div>
            <div class='section-title'>Síntomas</div><div class='content-box'>{sintomas}</div>
            <div class='section-title'>Tratamiento / Receta</div><div class='content-box receta-box'>{receta}</div>
            <div class='signature'><div class='line'></div><b>Firma y Sello Médico</b></div>
        </body></html>"""
        
        archivo_pdf = f"Consulta_Paciente_{id_paciente}.pdf"
        with open("temporal.html", "w", encoding="utf-8") as f: f.write(html_code)
        try:
            gtk_path = r"C:\Program Files\GTK3-Runtime-Win64\bin"
            if gtk_path not in os.environ["PATH"] and os.path.exists(gtk_path): os.environ["PATH"] += os.path.pathsep + gtk_path
            HTML("temporal.html").write_pdf(archivo_pdf)
            os.startfile(archivo_pdf)
        except Exception as e: print(f"Error PDF: {e}")
        finally: 
            if os.path.exists("temporal.html"): os.remove("temporal.html")

    def cerrar_consulta_pantalla():
        entrada_sintomas.delete("1.0", "end")
        entrada_diagnostico.delete("1.0", "end")
        entrada_receta.delete("1.0", "end")
        sub_frame_consulta.pack_forget() 
        frame_contenido_tabla.pack(fill="both", expand=True) 
        cargar_datos() 

    def guardar_consulta_sql():
        sintomas = entrada_sintomas.get("1.0", "end").strip()
        diagnostico = entrada_diagnostico.get("1.0", "end").strip()
        receta = entrada_receta.get("1.0", "end").strip()
        nombre = label_atendiendo.cget("text").replace("Atendiendo a: ", "")

        if not sintomas or not diagnostico: return

        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO historial_visitas (id_paciente, motivo_consulta, diagnostico, medicamentos) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (id_paciente_seleccionado[0], sintomas, diagnostico, receta))
                conexion.commit()
                generar_pdf(id_paciente_seleccionado[0], name:=nombre, sintomas=sintomas, diagnostico=diagnostico, receta=receta)
                cerrar_consulta_pantalla()
            except Exception as e: print(f"Error: {e}")
            finally: conexion.close()

    def mostrar_formulario_consulta():
        seleccion = tabla_pacientes.selection()
        if not seleccion: return
        valores = tabla_pacientes.item(seleccion[0], "values")
        
        id_paciente_seleccionado[0] = valores[0]
        nombre_completo = f"{valores[2]} {valores[3]}"
        
        label_atendiendo.configure(text=f"Atendiendo a: {nombre_completo}")
        
        frame_contenido_tabla.pack_forget()
        sub_frame_consulta.pack(fill="both", expand=True)

    # -----------------------------------------------------
    # ASISTENCIA EN LA BITÁCORA / HISTORIAL CLÍNICO
    # -----------------------------------------------------
    def cargar_historial_con_filtros():
        id_paciente = id_paciente_seleccionado[0]
        fecha_ini = entrada_fecha_inicio.get().strip()
        fecha_fin = entrada_fecha_fin.get().strip()

        for fila in tabla_historial.get_children():
            tabla_historial.delete(fila)

        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                # Filtrado estricto por fechas en MySQL utilizando BETWEEN
                if fecha_ini and fecha_fin:
                    sql = """SELECT fecha_visita, motivo_consulta, diagnostico, medicamentos 
                             FROM historial_visitas 
                             WHERE id_paciente = %s AND DATE(fecha_visita) BETWEEN %s AND %s 
                             ORDER BY fecha_visita DESC"""
                    cursor.execute(sql, (id_paciente, fecha_ini, fecha_fin))
                else:
                    sql = """SELECT fecha_visita, motivo_consulta, diagnostico, medicamentos 
                             FROM historial_visitas 
                             WHERE id_paciente = %s 
                             ORDER BY fecha_visita DESC"""
                    cursor.execute(sql, (id_paciente,))
                
                for r in cursor.fetchall():
                    tabla_historial.insert("", "end", values=r)
            except Exception as e:
                print(f"Error al filtrar historial: {e}")
            finally:
                conexion.close()

    def resetear_filtros_y_ver_todo():
        entrada_fecha_inicio.delete(0, "end")
        entrada_fecha_fin.delete(0, "end")
        cargar_historial_con_filtros()

    def mostrar_historial_clinico():
        seleccion = tabla_pacientes.selection()
        if not seleccion: return 
        valores = tabla_pacientes.item(seleccion[0], "values")
        
        id_paciente_seleccionado[0] = valores[0]
        nombre_paciente_global[0] = f"{valores[2]} {valores[3]}"
        
        label_historial_titulo.configure(text=f"HISTORIAL CLÍNICO: {nombre_paciente_global[0]} (ID: {id_paciente_seleccionado[0]})")
        
        resetear_filtros_y_ver_todo()
                
        frame_contenido_tabla.pack_forget()
        sub_frame_historial.pack(fill="both", expand=True)

    def cerrar_historial_pantalla():
        sub_frame_historial.pack_forget()
        frame_contenido_tabla.pack(fill="both", expand=True)

    def imprimir_reporte_historial():
        filas = tabla_historial.get_children()
        if not filas: return

        html_filas = ""
        for f in filas:
            valores = tabla_historial.item(f, "values")
            html_filas += f"""
            <tr>
                <td style="padding: 8px; border: 1px solid #cbd5e0; font-size: 10pt; text-align: center;">{valores[0]}</td>
                <td style="padding: 8px; border: 1px solid #cbd5e0; font-size: 10pt;">{valores[1]}</td>
                <td style="padding: 8px; border: 1px solid #cbd5e0; font-size: 10pt;">{valores[2]}</td>
                <td style="padding: 8px; border: 1px solid #cbd5e0; font-size: 10pt;">{valores[3]}</td>
            </tr>
            """

        html_reporte = f"""
        <html><head><meta charset='UTF-8'><style>
            @page {{ size: letter landscape; margin: 15mm 15mm; }}
            body {{ font-family: Arial, sans-serif; color: #2d3748; line-height: 1.5; }}
            .header {{ border-bottom: 3px solid #17a2b8; padding-bottom: 8px; margin-bottom: 15px; }}
            .title {{ font-size: 20pt; font-weight: bold; color: #17a2b8; text-transform: uppercase; margin: 0; }}
            .main-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            .main-table th {{ background-color: #f1f5f9; padding: 10px; border: 1px solid #cbd5e0; font-weight: bold; text-align: left; font-size: 11pt; }}
        </style></head><body>
            <div class='header'>
                <h1 class='title'>REPORTE DE BITÁCORA Y HISTORIAL CLÍNICO</h1>
                <p style="margin: 3px 0;"><b>Paciente:</b> {nombre_paciente_global[0]} (ID: {id_paciente_seleccionado[0]}) | <b>Fecha de Impresión:</b> {datetime.date.today().strftime('%d/%m/%Y')}</p>
            </div>
            <table class='main-table'>
                <thead>
                    <tr>
                        <th style="width: 18%; text-align: center;">Fecha y Hora</th>
                        <th style="width: 27%;">Síntomas / Motivo</th>
                        <th style="width: 27%;">Diagnóstico</th>
                        <th style="width: 28%;">Tratamiento / Receta</th>
                    </tr>
                </thead>
                <tbody>
                    {html_filas}
                </tbody>
            </table>
        </body></html>"""

        archivo_pdf = f"Historial_Clinico_ID_{id_paciente_seleccionado[0]}.pdf"
        with open("temp_historial.html", "w", encoding="utf-8") as f: f.write(html_reporte)
        try:
            gtk_path = r"C:\Program Files\GTK3-Runtime-Win64\bin"
            if gtk_path not in os.environ["PATH"] and os.path.exists(gtk_path): os.environ["PATH"] += os.path.pathsep + gtk_path
            HTML("temp_historial.html").write_pdf(archivo_pdf)
            os.startfile(archivo_pdf)
        except Exception as e: print(f"Error PDF Historial: {e}")
        finally: 
            if os.path.exists("temp_historial.html"): os.remove("temp_historial.html")

    # =====================================================
    # SECCIÓN DE CONTROL DE BOTONES EN LA PARTE INFERIOR
    # =====================================================
    boton_buscar = ctk.CTkButton(frame_buscador, text="Buscar", command=ejecutar_busqueda, width=90)
    boton_buscar.pack(side="left", padx=5)

    boton_cancelar_busca = ctk.CTkButton(frame_buscador, text="Limpiar", command=cargar_datos, fg_color="#721c24", width=90)
    boton_cancelar_busca.pack(side="left", padx=5)

    # Botones del formulario de consulta médica
    ctk.CTkButton(sub_frame_consulta, text="Guardar y Generar PDF Carta", fg_color="#28a745", command=guardar_consulta_sql).pack(pady=8)
    ctk.CTkButton(sub_frame_consulta, text="Cancelar Consulta", command=cerrar_consulta_pantalla).pack(pady=4)

    # PANEL INTEGRADO DE CONTROL PARA LA BITÁCORA (Filtros + Impresión + Volver)
    frame_botones_historial = ctk.CTkFrame(sub_frame_historial, fg_color="transparent")
    frame_botones_historial.pack(pady=15)

    ctk.CTkButton(frame_botones_historial, text="Filtrar Rango 🔍", command=cargar_historial_con_filtros, fg_color="#2b6cb0", width=120).pack(side="left", padx=6)
    ctk.CTkButton(frame_botones_historial, text="Ver Todo", command=resetear_filtros_y_ver_todo, fg_color="#4a5568", width=100).pack(side="left", padx=6)
    ctk.CTkButton(frame_botones_historial, text="Imprimir Historial 🖨️", command=imprimir_reporte_historial, fg_color="#28a745", width=140).pack(side="left", padx=6)
    ctk.CTkButton(frame_botones_historial, text="Volver al Listado", command=cerrar_historial_pantalla, fg_color="#343a40", width=120).pack(side="left", padx=6)

    # Botones de la vista principal (Abajo de la tabla)
    boton_nueva_consulta = ctk.CTkButton(frame_contenido_tabla, text="Iniciar Consulta Médica", command=mostrar_formulario_consulta, fg_color="#007bff")
    boton_nueva_consulta.pack(pady=4)

    boton_ver_historial = ctk.CTkButton(frame_contenido_tabla, text="Ver Historial Clínico 📅", command=mostrar_historial_clinico, fg_color="#17a2b8")
    boton_ver_historial.pack(pady=4)

    boton_volver_lista = ctk.CTkButton(frame_contenido_tabla, text="Volver al Menú", command=ir_a_menu)
    boton_volver_lista.pack(pady=4)

    return frame_lista, cargar_datos