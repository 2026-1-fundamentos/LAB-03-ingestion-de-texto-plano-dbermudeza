"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
import pandas as pd


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

    """
    filepath = "files/input/clusters_report.txt"
    records = []
    current_record = None

    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    separator_found = False
    for line in lines:
        if not separator_found:
            if line.strip().startswith("---"):
                separator_found = True
            continue

        if not line.strip():
            continue

        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$", line)
        if match:
            if current_record is not None:
                records.append(current_record)

            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(",", "."))
            principales = match.group(4).strip()
            current_record = {
                "cluster": cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "principales_palabras_clave": principales,
            }
            continue

        if current_record is not None:
            current_record["principales_palabras_clave"] += " " + line.strip()

    if current_record is not None:
        records.append(current_record)

    for record in records:
        keywords = record["principales_palabras_clave"]
        keywords = re.sub(r"\s+", " ", keywords)
        keywords = re.sub(r"\s*,\s*", ", ", keywords)
        keywords = keywords.strip()
        if keywords.endswith("."):
            keywords = keywords[:-1]
        record["principales_palabras_clave"] = keywords

    df = pd.DataFrame(records)
    return df
