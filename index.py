# ******************************************************************************************
# Manipulación de Arreglos Unidimensionales
# Arreglos unidimensionales, bucles for, condiciones if y validación de datos
# ******************************************************************************************

# Importaciones
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from datetime import datetime


# Configurar precisión para trabajar con números grandes
getcontext().prec = 80


# Función para cerrar el programa cuando el usuario escriba salir
def cerrar_programa():
    print("\nPrograma finalizado correctamente.")
    raise SystemExit


# Función para mostrar datos en formato tabla en la consola
def imprimir_tabla(encabezados, filas):
    filas = [[str(dato) for dato in fila] for fila in filas]

    anchos = []
    for i in range(len(encabezados)):
        ancho_maximo = len(encabezados[i])

        for fila in filas:
            if len(fila[i]) > ancho_maximo:
                ancho_maximo = len(fila[i])

        anchos.append(ancho_maximo)

    separador = "+-" + "-+-".join("-" * ancho for ancho in anchos) + "-+"

    print(separador)
    print("| " + " | ".join(f"{encabezados[i]:<{anchos[i]}}" for i in range(len(encabezados))) + " |")
    print(separador)

    for fila in filas:
        print("| " + " | ".join(f"{fila[i]:<{anchos[i]}}" for i in range(len(fila))) + " |")

    print(separador)



# Función para leer números usando Decimal
def leer_numero(mensaje):
    while True:
        dato = input(mensaje).strip().lower()

        if dato == "salir":
            cerrar_programa()

        try:
            # Permite el ingreso de números con punto o con coma decimal
            dato = dato.replace(",", ".")
            numero = Decimal(dato)
            return numero
        except InvalidOperation:
            print("Error: debe ingresar un número válido.")


# Función para formatear números
def formatear_numero(numero, decimales=2):
    if abs(numero) >= Decimal("1000"):
        numero_formateado = f"{numero:,.{decimales}f}"
        numero_formateado = numero_formateado.replace(",", "X").replace(".", ",").replace("X", ".")
        return numero_formateado

    elif numero == numero.to_integral_value():
        return str(numero.quantize(Decimal("1")))

    else:
        numero_formateado = format(numero.normalize(), "f")
        numero_formateado = numero_formateado.replace(".", ",")
        return numero_formateado


# Función para obtener la carpeta Descargas/Downloads
def obtener_carpeta_descargas():
    carpeta_downloads = Path.home() / "Downloads"

    if carpeta_downloads.exists():
        return carpeta_downloads

    carpeta_descargas = Path.home() / "Descargas"

    if carpeta_descargas.exists():
        return carpeta_descargas

    # En caso de que no encuentra la carpeta Descargas, guarda en la carpeta actual del proyecto
    return Path.cwd()


# Función para guardar los resultados en PDF
def guardar_pdf_resultados(
    filas_original,
    filas_inverso,
    encabezados_mayores_10,
    filas_mayores_10,
    filas_resumen
):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

    except ImportError:
        print("\nNo se pudo generar el PDF porque falta instalar la librería reportlab.")
        print("Instala el paquete ejecutando este comando en la consola:")
        print("py -m pip install reportlab")
        return

    try:
        carpeta_descargas = obtener_carpeta_descargas()

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_arreglos{fecha}.pdf"
        ruta_pdf = carpeta_descargas / nombre_archivo

        documento = SimpleDocTemplate(
            str(ruta_pdf),
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        estilos = getSampleStyleSheet()
        elementos = []

        elementos.append(Paragraph("Manipulación de Arreglos Unidimensionales", estilos["Title"]))
        elementos.append(Spacer(1, 12))

        elementos.append(Paragraph(
            "A continuación se muestra el resultado de procesar arreglos unidimensionales y recorrerlos mediante el bucle for, luego de la interacción con el usuario: ",
            estilos["Normal"]
        ))
        elementos.append(Spacer(1, 18))

        def agregar_tabla_pdf(titulo, encabezados, filas):
            elementos.append(Paragraph(titulo, estilos["Heading2"]))

            datos = [encabezados] + filas
            tabla = Table(datos)

            tabla.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))

            elementos.append(tabla)
            elementos.append(Spacer(1, 16))

        agregar_tabla_pdf(
            "Lista original",
            ["Posición", "Número"],
            filas_original
        )

        agregar_tabla_pdf(
            "Números en orden inverso",
            ["Orden", "Número"],
            filas_inverso
        )

        agregar_tabla_pdf(
            "Números mayores que 10",
            encabezados_mayores_10,
            filas_mayores_10
        )

        agregar_tabla_pdf(
            "Resumen final",
            ["Descripción", "Resultado"],
            filas_resumen
        )

        documento.build(elementos)

        print("\nPDF generado correctamente.")
        print(f"Ubicación del archivo: {ruta_pdf}")

    except PermissionError:
        print("\nError: no se pudo guardar el PDF.")
        print("Verifique que tenga permisos para escribir en la carpeta Descargas.")

    except OSError as error:
        print("\nError del sistema al intentar guardar el PDF.")
        print(f"Detalle del error: {error}")

    except Exception as error:
        print("\nOcurrió un error inesperado al generar el PDF.")
        print(f"Detalle del error: {error}")


# Función para procesar la lógica principal del sistema
try:
    print("\nEscriba 'salir' en cualquier momento para cerrar el programa.\n")

    numeros = []

    while True:
        try:
            dato = input("¿Cuántos números desea ingresar? Mínimo 5: ").strip().lower()

            if dato == "salir":
                cerrar_programa()

            cantidad = int(dato)

            if cantidad >= 5:
                break
            else:
                print("Debe ingresar al menos 5 números.")

        except ValueError:
            print("Error: debe ingresar un número entero válido.")


    for i in range(cantidad):
        numero = leer_numero(f"Ingrese el número {i + 1}: ")
        numeros.append(numero)


    if len(numeros) > 0:

        print("\n******** RESULTADOS ********")

        # Muestra la lista original de números ingresada por el usuario
        filas_original = []

        for i in range(len(numeros)):
            filas_original.append([
                i + 1,
                formatear_numero(numeros[i])
            ])

        print("\nLista original:")
        imprimir_tabla(
            ["Posición", "Número"],
            filas_original
        )

        # Muestra la lista original de números ingresada por el usuario pero en orden inverso
        filas_inverso = []

        for i in range(len(numeros) - 1, -1, -1):
            filas_inverso.append([
                len(numeros) - i,
                formatear_numero(numeros[i])
            ])

        print("\nNúmeros en orden inverso:")
        imprimir_tabla(
            ["Orden", "Número"],
            filas_inverso
        )

        # Muestra los números mayores que 10 de la lista original de números ingresada por el usuario
        filas_mayores_10 = []
        cantidad_mayores_10 = 0

        for numero in numeros:
            if numero > Decimal("10"):
                cantidad_mayores_10 += 1
                filas_mayores_10.append([
                    cantidad_mayores_10,
                    formatear_numero(numero)
                ])

        print("\nNúmeros mayores que 10:")

        if len(filas_mayores_10) > 0:
            encabezados_mayores_10 = ["N°", "Número mayor que 10"]
            filas_resultado_mayores_10 = filas_mayores_10
        else:
            encabezados_mayores_10 = ["Mensaje"]
            filas_resultado_mayores_10 = [["No existen números mayores que 10"]]

        imprimir_tabla(
            encabezados_mayores_10,
            filas_resultado_mayores_10
        )

        # Muestra la suma total de la lista original de números ingresada por el usuario
        suma_total = Decimal("0")

        for numero in numeros:
            suma_total += numero

       
        # Muestra el resumen final de todo el proceso realizado
        filas_resumen = [
            ["Suma total de los elementos", formatear_numero(suma_total)],
            ["Cantidad de números mayores que 10", cantidad_mayores_10]
        ]

        print("\nResumen final:")
        imprimir_tabla(
            ["Descripción", "Resultado"],
            filas_resumen
        )

        # Muestra el resumen final de todo el proceso realizado
        guardar_pdf_resultados(
            filas_original,
            filas_inverso,
            encabezados_mayores_10,
            filas_resultado_mayores_10,
            filas_resumen
        )

    else:
        print("La lista está vacía. No se pueden realizar operaciones.")

except KeyboardInterrupt:
    print("\n\nPrograma finalizado correctamente")