Sello PDF Automático 📄🖋️

Este proyecto es una herramienta de escritorio desarrollada en Python que permite estampar un sello de "RECIBIDO" dinámico en la primera página de cualquier archivo PDF. El sello incluye la fecha actual del sistema en español, se genera con un aspecto realista y se posiciona automáticamente en la esquina inferior derecha del documento.

✨ Características

Interfaz Gráfica (GUI): Ventanas nativas para seleccionar archivos y carpetas de destino de forma sencilla.

Sello Dinámico: Genera una imagen en tiempo real con la fecha del día formateada en español (ej. 13 ENE 2026).

Estilo Realista: El sello presenta un borde azul, texto en negrita, línea punteada y la fecha en color rojo, con una ligera rotación para simular el impacto de un sello manual.

Posicionamiento Inteligente: El sello se coloca siempre en la esquina inferior derecha, calculando automáticamente las dimensiones de la página (A4, Carta, Oficio, etc.).

Renombrado Automático: Sugiere guardar el archivo con el sufijo _sellado para no sobrescribir el original.

Privacidad: Todo el proceso ocurre en la memoria RAM; no se guardan imágenes temporales en el disco duro.

🛠️ Requisitos previos

Para ejecutar este programa, necesitas tener instalado Python 3.x en tu sistema.

Dependencias

El proyecto utiliza las siguientes librerías de terceros:

PyMuPDF (fitz): Para la manipulación y edición de archivos PDF.

Pillow (PIL): Para la creación y renderizado de la imagen del sello.

🚀 Instalación

Clona este repositorio:

git clone [https://github.com/DarkUnknowKnigth/sello-pdf-python.git](https://github.com/DarkUnknowKnigth/sello-pdf-python.git)
cd sello-pdf-python


Instala las dependencias necesarias usando el archivo requirements.txt:

pip install -r requirements.txt


📖 Uso

Simplemente ejecuta el script principal:

python stamp_app.py


Seleccionar: Se abrirá una ventana para elegir el archivo PDF original.

Guardar: Se abrirá una segunda ventana sugiriendo el nombre [nombre_original]_sellado.pdf. Selecciona la carpeta donde deseas guardarlo.

Resultado: El programa aplicará el sello y te notificará cuando el proceso haya terminado con éxito.

📁 Estructura del Proyecto

.
├── stamp_app.py        # Código fuente principal del programa
├── requirements.txt    # Listado de librerías necesarias
└── README.md           # Documentación del proyecto (este archivo)


🤝 Contribuciones

Si deseas mejorar el diseño del sello, añadir procesamiento por lotes o soporte para sellos personalizados, ¡las contribuciones son bienvenidas!

Haz un Fork del proyecto.

Crea una rama para tu mejora (git checkout -b feature/MejoraIncreible).

Haz un Commit de tus cambios (git commit -m 'Añadir nueva funcionalidad').

Haz un Push a la rama (git push origin feature/MejoraIncreible).

Abre un Pull Request.

Desarrollado con ❤️ por DarkUnknowKnigth