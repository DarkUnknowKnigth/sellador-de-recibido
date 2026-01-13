import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def crear_imagen_sello():
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
        font_titulo = ImageFont.truetype("arialbd.ttf", 90) 
        font_fecha = ImageFont.truetype("arial.ttf", 55)
    except:
        # Si falla, usamos la fuente por defecto
        font_titulo = ImageFont.load_default()
        font_fecha = ImageFont.load_default()

    # 1. Dibujar el marco azul
    draw.rectangle([20, 20, 580, 330], outline=color_azul, width=10)
    
    # 2. Dibujar "RECIBIDO" en azul y negrita
    draw.text((width//2, 100), "RECIBIDO", fill=color_azul, font=font_titulo, anchor="mm")
    
    # 3. Dibujar línea punteada central
    for x in range(60, 540, 20):
        draw.line([x, 180, x+10, 180], fill=color_azul, width=3)
    
    # 4. Dibujar Fecha en rojo (Formato español forzado)
    ahora = datetime.now()
    meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    fecha_espanol = f"{ahora.day} {meses[ahora.month-1]} {ahora.year}"
    
    draw.text((width//2, 240), fecha_espanol, fill=color_rojo, font=font_fecha, anchor="mm")
    
    # 5. Aplicar una rotación ligera para realismo (sello manual)
    img = img.rotate(12, resample=Image.BICUBIC, expand=True)
    
    # Guardar en buffer
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def procesar_archivo():
    """Maneja la lógica de la interfaz y el procesamiento del PDF."""
    root = tk.Tk()
    root.withdraw() 

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
        # Generar sello
        sello_bytes = crear_imagen_sello()
        
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

if __name__ == "__main__":
    procesar_archivo()