import customtkinter as ctk
from tkinter import ttk
from database import conectar_db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def obtener_metricas_reales():
    # Valores por defecto por si falla la conexión
    total_pacientes = 0
    total_citas = 0
    hombres = 50
    mujeres = 50
    
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            # 1. Contar pacientes totales
            cursor.execute("SELECT COUNT(*) FROM pacientes")
            total_pacientes = cursor.fetchone()[0]

            # 2. Contar citas totales agendadas
            cursor.execute("SELECT COUNT(*) FROM citas")
            total_citas = cursor.fetchone()[0]

            # 3. Contar hombres y mujeres para la gráfica
            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE genero = 'Male'")
            hombres = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE genero = 'Female'")
            mujeres = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al leer métricas: {e}")
        finally:
            conexion.close()
            
    return total_pacientes, total_citas, hombres, mujeres

def crear_vista_dashboard(ventana):
    frame_dash = ctk.CTkScrollableFrame(ventana, fg_color="#0f172a", corner_radius=0)

    # Traer los datos vivos de la Base de Datos
    num_pacientes, num_citas_totales, cant_hombres, cant_mujeres = obtener_metricas_reales()

    # Título de Bienvenida
    lbl_bienvenida = ctk.CTkLabel(frame_dash, text="Bienvenido, Dr. Roberto Rosales", font=("Arial", 26, "bold"), text_color="white")
    lbl_bienvenida.pack(pady=(30, 20), padx=30, anchor="w")

    # --- CONTENEDOR DE TARJETAS ---
    frame_cards = ctk.CTkFrame(frame_dash, fg_color="transparent")
    frame_cards.pack(fill="x", padx=30, pady=10)

    def crear_tarjeta(parent, titulo, valor, color_borde):
        card = ctk.CTkFrame(parent, fg_color="#1e293b", border_width=2, border_color=color_borde, height=120)
        card.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(card, text=titulo, font=("Arial", 14), text_color="#94a3b8").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=str(valor), font=("Arial", 32, "bold"), text_color="white").pack(pady=(5, 15))
        return card

    # Tarjetas requeridas
    crear_tarjeta(frame_cards, "Total Pacientes", num_pacientes, "#7ED9A1")
    crear_tarjeta(frame_cards, "Citas Programadas", num_citas_totales, "#3b82f6")
    crear_tarjeta(frame_cards, "Consultas Hoy", "9", "#8b5cf6")

    # --- DISTRIBUCIÓN INFERIOR: TABLA (Izquierda) y GRÁFICA (Derecha) ---
    frame_inferior = ctk.CTkFrame(frame_dash, fg_color="transparent")
    frame_inferior.pack(fill="both", expand=True, padx=30, pady=20)

    # Lado Izquierdo: Próximas Citas (Le asignamos expand=True para que comparta el espacio de forma justa)
    frame_izq = ctk.CTkFrame(frame_inferior, fg_color="transparent")
    frame_izq.pack(side="left", fill="both", expand=True, padx=(0, 15))

    lbl_proximas = ctk.CTkLabel(frame_izq, text="Próximas Citas Agendadas", font=("Arial", 18, "bold"), text_color="white")
    lbl_proximas.pack(anchor="w", pady=(0, 10))

    frame_tabla = ctk.CTkFrame(frame_izq, fg_color="#1e293b", corner_radius=15)
    frame_tabla.pack(fill="both", expand=True)

    columnas = ("Hora", "Paciente", "Motivo")
    tabla_resumen = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
    
    style = ttk.Style()
    style.configure("Treeview", background="#1e293b", foreground="white", fieldbackground="#1e293b", borderwidth=0)
    tabla_resumen.heading("Hora", text="Hora")
    tabla_resumen.heading("Paciente", text="Paciente")
    tabla_resumen.heading("Motivo", text="Motivo")
    
    tabla_resumen.column("Hora", width=80, minwidth=60, anchor="center")
    tabla_resumen.column("Paciente", width=180, minwidth=140, anchor="w")
    tabla_resumen.column("Motivo", width=200, minwidth=160, anchor="w")
    
    # Cargar citas reales de la BD a la tablita resumen
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT hora, paciente, motivo FROM citas ORDER BY id DESC LIMIT 5")
            for fila in cursor.fetchall():
                tabla_resumen.insert("", "end", values=fila)
        except: pass
        finally: conexion.close()

    tabla_resumen.pack(fill="both", expand=True, padx=15, pady=15)

    # =========================================================================
    # Lado Derecho: Gráfica de Pastel (¡AQUÍ ESTÁ EL CAMBIO DE ESPACIO!)
    # =========================================================================
    # Quitamos el 'width=320' fijo para que no se asfixie el cuadro y le agregamos expand=True
    frame_der = ctk.CTkFrame(frame_inferior, fg_color="#1e293b", corner_radius=15)
    frame_der.pack(side="right", fill="both", expand=True, padx=(15, 0))

    lbl_grafica = ctk.CTkLabel(frame_der, text="Distribución por Género", font=("Arial", 16, "bold"), text_color="white")
    lbl_grafica.pack(pady=15)

    # Crear Gráfica de Pastel con Matplotlib (Aumentamos ligeramente el figsize a 3.5 para darle más aire)
    fig, ax = plt.subplots(figsize=(3.5, 3.5), facecolor="#1e293b")
    
    labels = ['Hombres', 'Mujeres']
    sizes = [cant_hombres if cant_hombres > 0 else 1, cant_mujeres if cant_mujeres > 0 else 1]
    colors = ['#3b82f6', '#7ED9A1'] 

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
           textprops={'color': "white", 'fontsize': 11}, colors=colors)
    ax.axis('equal')  

    # Integrar gráfico de Matplotlib en el contenedor de CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_der)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=(10, 20), padx=20, fill="both", expand=True)
    plt.close(fig) 

    return frame_dash