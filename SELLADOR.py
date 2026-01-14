import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def crear_imagen_sello(nombre_receptor=""):
    """Genera una imagen de sello realista con texto azul y fecha roja en español."""
    # Configuración de colores
    color_azul = (0, 51, 153, 255)  # Azul sello
    color_rojo = (200, 0, 0, 255)   # Rojo fecha
    
    # Crear un lienzo grande para alta calidad antes de rotar
    width, height = 600, 350
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Intentar cargar fuentes del sistema (Windows/Mac/Linux)
    try:
        # Intentamos cargar Arial Bold para el "RECIBIDO"
        font_grande = ImageFont.truetype("arialbd.ttf", 70) 
        font_pequena = ImageFont.truetype("arialbd.ttf", 35)
        font_chiquita = ImageFont.truetype("arialbd.ttf", 25)
        font_fecha = ImageFont.truetype("arial.ttf", 40)
    except:
        # Si falla, usamos la fuente por defecto
        font_grande = ImageFont.load_default()
        font_pequena = ImageFont.load_default()
        font_fecha = ImageFont.load_default()

    # 1. Dibujar el marco azul
    draw.rectangle([20, 20, 580, 330], outline=color_azul, width=10)
    
    # 2. Dibujar "RECIBIDO" en azul y negrita
    
    draw.text((width//2, 48), "UNACH", fill=color_azul, font=font_pequena, anchor="mm")
    draw.text((width//2, 82), "DIRECCIÓN DE SERVICIOS ESCOLARES", fill=color_azul, font=font_chiquita, anchor="mm")
    draw.text((width//2, 127), "RECIBIDO", fill=color_azul, font=font_grande, anchor="mm")
    draw.text((width//2, 174), "DIRECCIÓN", fill=color_azul, font=font_pequena, anchor="mm")
    
    # 3. Dibujar línea punteada central
    for x in range(60, 540, 20):
        draw.line([x, 195, x+10, 195], fill=color_azul, width=3)
    
    # 4. Dibujar Fecha en rojo (Formato español forzado)
    ahora = datetime.now()
    meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    fecha_espanol = f"{ahora.day} {meses[ahora.month-1]} {ahora.year} {ahora.hour:02}:{ahora.minute:02}"
    
    draw.text((width//2, 240), fecha_espanol, fill=color_rojo, font=font_fecha, anchor="mm")
    
    # 5. Dibujar Nombre del Receptor (si existe)
    if nombre_receptor:
        tamano_nombre = 30
        try:
            font_nombre = ImageFont.truetype("arial.ttf", tamano_nombre)
            # Ajustar tamaño si el nombre es muy largo para que quepa (max 560px)
            while font_nombre.getlength(nombre_receptor) > 560 and tamano_nombre > 10:
                tamano_nombre -= 2
                font_nombre = ImageFont.truetype("arial.ttf", tamano_nombre)
        except:
            font_nombre = ImageFont.load_default()
            
        draw.text((width//2, 290), nombre_receptor, fill=color_azul, font=font_nombre, anchor="mm")

    # 5. Aplicar una rotación ligera para realismo (sello manual)
    img = img.rotate(12, resample=Image.BICUBIC, expand=True)
    
    # Guardar en buffer
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def procesar_archivo():
    """Maneja la lógica de la interfaz y el procesamiento del PDF."""
    # 1. Seleccionar archivo de entrada
    ruta_entrada = filedialog.askopenfilename(
        title="Selecciona el archivo PDF original",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    
    if not ruta_entrada:
        return

    # 2. Preparar nombres
    directorio = os.path.dirname(ruta_entrada)
    nombre_base = os.path.splitext(os.path.basename(ruta_entrada))[0]
    nombre_sugerido = f"{nombre_base}_sellado.pdf"

    # 3. Guardar como...
    ruta_salida = filedialog.asksaveasfilename(
        title="Guardar PDF sellado como...",
        initialdir=directorio,
        initialfile=nombre_sugerido,
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    
    if not ruta_salida:
        return

    try:
        # Leer nombre desde nombre.txt
        nombre_receptor = ""
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        ruta_txt = os.path.join(base_path, "nombre.txt")
        if os.path.exists(ruta_txt):
            try:
                with open(ruta_txt, "r", encoding="utf-8") as f:
                    nombre_receptor = f.read().strip()
            except UnicodeDecodeError:
                with open(ruta_txt, "r", encoding="latin-1") as f:
                    nombre_receptor = f.read().strip()
        else:
            messagebox.showwarning("Atención", f"No se encontró el archivo 'nombre.txt'.\nVerifica que no se llame 'nombre.txt.txt' y esté junto al EXE.\n\nRuta buscada:\n{ruta_txt}")

        # Generar sello
        sello_bytes = crear_imagen_sello(nombre_receptor)
        
        # Abrir PDF
        doc = fitz.open(ruta_entrada)
        if len(doc) == 0:
            raise Exception("El archivo PDF está vacío o dañado.")
            
        pagina = doc[0]
        
        # Obtener dimensiones de la página
        p_width = pagina.rect.width
        p_height = pagina.rect.height
        
        # Definir tamaño del sello en el PDF y margen
        ancho_sello = 180
        alto_sello = 100
        margen = 40
        
        # Calcular coordenadas para la parte inferior derecha
        rect_destino = fitz.Rect(
            p_width - ancho_sello - margen, 
            p_height - alto_sello - margen, 
            p_width - margen, 
            p_height - margen
        )
        
        pagina.insert_image(rect_destino, stream=sello_bytes)
        
        doc.save(ruta_salida)
        doc.close()
        
        messagebox.showinfo("Proceso Exitoso", f"El sello se aplicó correctamente en:\n{os.path.basename(ruta_salida)}")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{str(e)}")

def iniciar_interfaz():
    """Crea la ventana principal de la aplicación que se mantiene abierta."""
    ventana = tk.Tk()
    ventana.title("Sellador de Recibido")
    ventana.geometry("400x220")
    
    tk.Label(ventana, text="Sistema de Sellado Digital", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Label(ventana, text="Haz clic abajo para seleccionar y sellar un PDF:").pack()
    
    # Botón que ejecuta la función de procesar
    btn = tk.Button(ventana, text="Seleccionar PDF", command=procesar_archivo, bg="#003399", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    btn.pack(pady=20)
    
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()