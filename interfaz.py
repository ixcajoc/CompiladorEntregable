from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Archivo import SQLPaser

objetoAbrir = SQLPaser()

def insertarContenido():
    limpiarContenido()
    info = objetoAbrir.abrirArchivo()
    txtCargarArchivo.delete("1.0", tk.END)
    txtCargarArchivo.insert(tk.END, info)
    enumerar2()

def obtenerInfo():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    if infoActual == "\n":
        tk.messagebox.showerror("Ningún Archivo Cargado",
                                "Aún no ha cargado o escrito alguna instruccion")
        return
    else:
        objetoAbrir.contenido = infoActual

def analize_file():
    obtenerInfo()
    # enumerar()
    objetoAbrir.analizadorSintactico()
    # txtConvertirArchivo.delete("1.0", tk.END)
    llenarTabla()

def EstadoExportar():
    if objetoAbrir.listaErrores:
        subMenuTokens.entryconfig("Exportar", state="disabled")
    else:
        subMenuTokens.entryconfig("Exportar", state="normal")

def exportarSQL():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.exportarSQL(infoActual)


def Guardar():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.marcarCambios(infoActual)
    objetoAbrir.guardarArchivo(infoActual)

def guardarComo():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.guardarArchivoComo(infoActual)

def cerrar():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.marcarCambios(infoActual)

    interfaz.quit()

    
def limpiarContenido():
    # txtConvertirArchivo.delete("1.0", tk.END)
    txtCargarArchivo.delete("1.0", tk.END)
    # txtlineaNumerica.config(state="normal")
    txtlineaNumerica2.config(state="normal")
    # txtlineaNumerica.delete("1.0", tk.END)
    txtlineaNumerica2.delete("1.0", tk.END)
    objetoAbrir.limpiarVariables()
    tabla.delete(*tabla.get_children())


def enumerar2():
    txtlineaNumerica2.config(state="normal")
    txtlineaNumerica2.delete("1.0", tk.END)

    for i in range(1,objetoAbrir.cantidadLineas+1):
        txtlineaNumerica2.insert(tk.END, f"{i}\n")
    txtlineaNumerica2.config(state="disabled")

def llenarTabla():
    tabla.delete(*tabla.get_children())
    for clave, valor in objetoAbrir.listaErrores.items():
        tabla.insert("", "end", values=(clave,valor))
    EstadoExportar()
    objetoAbrir.listaErrores = {}

def colorear_linea(numLinea):
    # txtConvertirArchivo.tag_remove("coloreada", "1.0", "end")
    txtCargarArchivo.tag_remove("coloreada", "1.0", "end")

    linea = int(numLinea)
    # txtConvertirArchivo.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    txtCargarArchivo.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    # txtlineaNumerica.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    txtlineaNumerica2.tag_add("coloreada", f"{linea}.0", f"{linea}.end")
    
def seleccionar_fila(event):
    item = tabla.selection()[0]  #obtener el índice de la fila seleccionada
    numero_linea, nombre_error = tabla.item(item, "values")
    colorear_linea(numero_linea)


interfaz = tk.Tk()
interfaz.title("Automatas")
interfaz.geometry("1366x768")
interfaz.attributes('-fullscreen', True)
interfaz.config(background="white")

barraMenu = tk.Menu(interfaz)

subMenuArchivo = tk.Menu(barraMenu, tearoff=0)
subMenuArchivo.add_command(label="Abrir",command=insertarContenido)
subMenuArchivo.add_command(label="Guardar", command=Guardar)
subMenuArchivo.add_command(label="Guardar como...", command=guardarComo)
subMenuArchivo.add_command(label="Limpiar contenido", command=limpiarContenido)

subMenuTokens = tk.Menu(barraMenu, tearoff=0)
subMenuTokens.add_command(label="Analizador", command=analize_file)  
subMenuTokens.add_command(label="Exportar", command= exportarSQL ,state="disabled")

subMenuSalir = tk.Menu(barraMenu, tearoff=0)
# subMenuSalir.add_command(label="Cerrar Programa",command=interfaz.destroy)  
subMenuSalir.add_command(label="Cerrar Programa",command=cerrar)  

#hago los menus
barraMenu.add_cascade(label="Archivo", menu=subMenuArchivo)
barraMenu.add_cascade(label="Opciones", menu=subMenuTokens)
barraMenu.add_cascade(label="Salir", menu=subMenuSalir)

interfaz.config(menu=barraMenu)

txtCargarArchivo = tk.Text(interfaz, wrap="none", width=155, height=26,font=("Century Gothic", 11),
                           highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtCargarArchivo.place(x= 30, y = 10)
txtCargarArchivo.config(padx=10,pady=10)
txtCargarArchivo.tag_configure("coloreada", background="yellow", foreground="black")



txtlineaNumerica2 = tk.Text(interfaz, wrap="none", width=3, height=26,font=("Century Gothic", 11),
                           highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtlineaNumerica2.place(x= 10, y=10)
txtlineaNumerica2.config(pady=10, fg="red")


#sincronizar scroll de cajas
def sincornizar(txtOrigen, txtDestino):
    def sincroDesplazamiento(*args):
        fraccion = txtOrigen.yview()[0]
        txtDestino.yview_moveto(fraccion)

    return sincroDesplazamiento

sincroConvertirAlinea = sincornizar(txtCargarArchivo,txtlineaNumerica2)
sincroLineaAconvertir = sincornizar(txtCargarArchivo, txtlineaNumerica2)
sincroCargarLineaConvertir = sincornizar(txtCargarArchivo,txtlineaNumerica2)
sincroLinea2CargarLineaConvertir = sincornizar(txtlineaNumerica2,txtCargarArchivo)

txtCargarArchivo.config(yscrollcommand=sincroCargarLineaConvertir)
txtlineaNumerica2.config(yscrollcommand=sincroLinea2CargarLineaConvertir)



#inicio de mi tabla
tabla = ttk.Treeview(interfaz, columns=("Número de Línea", "Nombre de Error"))
tabla.bind("<<TreeviewSelect>>", seleccionar_fila)  # Asociar evento de selección
tabla['height'] = 7

style = ttk.Style()
style.configure('Treeview', font=("Century Gothic", 11 ), foreground='black' )
style.configure('Treeview.Heading', font=('Century Gothic', 13), foreground='black')

tabla.heading("#1", text="Número de Línea")
tabla.heading("#2", text="Nombre de Error")

tabla.column("#0", width=0)
tabla.column("#1", width=200,anchor="center")
tabla.column("#2", width=1145,anchor="w")


tabla.place(x = 10,y=560)


interfaz.mainloop()
