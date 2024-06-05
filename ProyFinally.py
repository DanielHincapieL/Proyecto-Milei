import pandas as pd
import os
import logging
import platform
import time
from datetime import datetime
import numpy as np  # Importa numpy para trabajar con valores NaN

def configurar_registro():
    # Configuración del registro de eventos
    log_filename = 'procedimientos.log'
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(message)s'
    )

def registrar_encabezado():
    # Encabezado del log
    user = os.getlogin()
    system_info = platform.uname()
    header = f"Usuario: {user}\nSistema Operativo: {system_info.system}\n" \
             f"Plataforma: {platform.platform()}\n" \
             f"Version: {system_info.version}\n" \
             f"Procesador: {system_info.processor}\n"
    logging.info(header)

def leer_datos_estudiantes(file_path):
    # Leer el archivo Excel que contiene la información de los estudiantes
    return pd.read_excel(file_path)

def leer_asignaturas(file_path):
    # Leer el archivo Excel que contiene la información de las asignaturas
    asignaturas_df = pd.read_excel(file_path)
    asignaturas = {}
    for index, row in asignaturas_df.iterrows():
        asignatura = row['nombre']
        codigo = asignatura[:3].upper() + str(row['creditos']) + str(row['nivel'])
        horas_docente = calcular_horas_docente(row['creditos'])
        horas_independiente = calcular_horas_independiente(row['creditos'])
        asignaturas[codigo] = {
            'nombre': row['nombre'],
            'creditos': row['creditos'],
            'nivel': row['nivel'],
            'horas_docente': horas_docente,
            'horas_independiente': horas_independiente
        }
    return asignaturas

def calcular_horas_docente(creditos):
    if creditos == 12:
        return 192
    elif creditos == 4:
        return 96
    elif creditos == 3:
        return 64
    elif creditos == 2:
        return 32
    elif creditos == 1:
        return 16
    else:
        return 0  # Valor predeterminado si no coincide con ninguno de los casos

def calcular_horas_independiente(creditos):
    if creditos == 12:
        return 384
    elif creditos == 4:
        return 120
    elif creditos == 3:
        return 80
    elif creditos == 2:
        return 64
    elif creditos == 1:
        return 32
    else:
        return 0  # Valor predeterminado si no coincide con ninguno de los casos


def crear_estructura_archivos(df, asignaturas, cupos_por_semestre, carpeta_principal):
    # Verifica y maneja los valores NaN en el DataFrame
    df.fillna('', inplace=True)  # Reemplaza NaN con una cadena vacía

    # Crear las carpetas correspondientes para las asignaturas y los grupos
    for asignatura, info in asignaturas.items():
        semestre = info['nivel']
        carpeta_semestre = os.path.join(carpeta_principal, f"Semestre {semestre}")
        carpeta_asignatura = os.path.join(carpeta_semestre, asignatura)
        if not os.path.exists(carpeta_asignatura):
            os.makedirs(carpeta_asignatura)

        estudiantes_semestre = df[df['Semestre'] == semestre]
        cupo = cupos_por_semestre[semestre]
        grupos_estudiantes = [estudiantes_semestre[i * cupo:(i + 1) * cupo] for i in range(len(estudiantes_semestre) // cupo + (len(estudiantes_semestre) % cupo > 0))]

        for i, grupo in enumerate(grupos_estudiantes):
            nombre_grupo = f"{asignatura}{i + 1}"
            ruta_grupo_csv = os.path.join(carpeta_asignatura, nombre_grupo + ".csv")
            ruta_grupo_xlsx = os.path.join(carpeta_asignatura, nombre_grupo + ".xlsx")

            grupo = grupo.fillna('')  # Reemplaza NaN con una cadena vacía en el grupo

            grupo.to_csv(ruta_grupo_csv, index=False)
            with open(ruta_grupo_csv, 'a') as f:
                f.write(f"\nInformación del Curso\n")
                f.write(f"Código: {asignatura}\n")
                f.write(f"Nombre: {info['nombre']}\n")
                f.write(f"Cupos: {cupo}\n")
                f.write(f"Créditos: {info['creditos']}\n")
                f.write(f"Horas Docente: {info['horas_docente']}\n")
                f.write(f"Horas Independiente: {info['horas_independiente']}\n")
                f.write(f"Cantidad de Estudiantes: {len(grupo)}\n")
                f.write(f"Total de Grupos: {len(grupos_estudiantes)}\n")
                f.write(f"Fecha de Creación: {datetime.now().strftime('%Y%m%d')}\n")

            with pd.ExcelWriter(ruta_grupo_xlsx, engine='xlsxwriter') as writer:
                grupo.to_excel(writer, sheet_name='Estudiantes', index=False)
                workbook  = writer.book
                worksheet = workbook.add_worksheet('Información del Curso')
                writer.sheets['Información del Curso'] = worksheet

                info_curso = [
                    ["Código", asignatura],
                    ["Nombre", info['nombre']],
                    ["Cupos", cupo],
                    ["Créditos", info['creditos']],
                    ["Horas Docente", info['horas_docente']],
                    ["Horas Independiente", info['horas_independiente']],
                    ["Cantidad de Estudiantes", len(grupo)],
                    ["Total de Grupos", len(grupos_estudiantes)],
                    ["Fecha de Creación", datetime.now().strftime('%Y%m%d')]
                ]
                for row_num, (key, value) in enumerate(info_curso):
                    worksheet.write(row_num, 0, key)
                    worksheet.write(row_num, 1, value)

def resumen_final(contar_archivos, mover_archivos, renombrar_archivos):
    # Resumen final en el log
    logging.info(f"\nResumen de procedimientos realizados:\n")
    logging.info(f"Total de archivos contados: {contar_archivos}")
    logging.info(f"Total de archivos movidos: {mover_archivos}")
    logging.info(f"Total de archivos renombrados: {renombrar_archivos}")

def ejecutar_procedimientos():
    configurar_registro()
    registrar_encabezado()

    # Definir la carpeta principal
    carpeta_principal = "Semestres"

    # Leer los datos de los estudiantes
    df = leer_datos_estudiantes(pd.read_excel, 'https://github.com/DanielHincapieL/Proyecto-Milei/raw/5b623c2049906aa00239524585f2d8a9db98c3d5/Students.xlsx')

    # Leer el diccionario de asignaturas desde el archivo Excel
    asignaturas = leer_asignaturas(pd.read_excel, 'https://github.com/DanielHincapieL/Proyecto-Milei/raw/5b623c2049906aa00239524585f2d8a9db98c3d5/asignaturas.xlsx')

    # Diccionario de cupos por semestre
    cupos_por_semestre = {
        1: 30,
        2: 30,
        3: 30,
        4: 25,
        5: 25,
        6: 25,
        7: 20,
        8: 20,
        9: 20,
        10: 10
    }

    contar_archivos = 0
    mover_archivos = 0
    renombrar_archivos = 0

    # Crear la estructura de archivos
    crear_estructura_archivos(df, asignaturas, cupos_por_semestre, carpeta_principal)

    resumen_final(contar_archivos, mover_archivos, renombrar_archivos)
    print("Se ha completado el proceso y registrado en el log.")

if __name__ == "__main__":
    ejecutar_procedimientos()