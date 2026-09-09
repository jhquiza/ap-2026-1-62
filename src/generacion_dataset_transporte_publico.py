import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(101)
n_rows = 1140  # Se agregarán 60 duplicados para llegar a 1.200

# 1. Catálogos base
estaciones = [
    "San Antonio", "Poblado", "Niquía", "Itagüí", "Acevedo",
    "San Javier", "Berrío", "Alpujarra", "Estadio", "Universidad"
]

rutas_modos = [
    ("Línea A", "Metro"),
    ("Línea B", "Metro"),
    ("Línea K", "Teleférico/Cable"),
    ("Línea J", "Teleférico/Cable"),
    ("Línea T", "Tranvía"),
    ("Troncal 1", "BRT/Bus"),
    ("Pretroncal 2", "BRT/Bus")
]

perfiles = ["Frecuente", "Estudiantil", "Adulto Mayor", "PCD (Discapacidad)", "Ocasional"]
medios_pago = ["Tarjeta Cívica/SmartCard", "Código QR Móvil", "Bancaria Contactless"]

# 2. Generación de registros sintéticos
records = []
start_date = datetime(2026, 1, 15)

for i in range(1, n_rows + 1):
    id_val = f"VAL-{20260000 + i}"
    id_tarjeta = f"CRD-{np.random.randint(10000, 10500)}"  # 500 tarjetas recurrentes
    
    # Suciedad en Estación (espacios y mayúsculas/minúsculas)
    est = np.random.choice(estaciones)
    r_case = np.random.rand()
    if r_case < 0.25:
        est_dirty = est.upper()
    elif r_case < 0.50:
        est_dirty = est.lower()
    elif r_case < 0.75:
        est_dirty = f"  {est} "
    else:
        est_dirty = est

    # Suciedad en Ruta y Modo (columna combinada con distintos delimitadores)
    ruta, modo = rutas_modos[np.random.choice(len(rutas_modos))]
    sep = np.random.choice([" - ", " / ", " | "])
    ruta_modo_dirty = f"{ruta}{sep}{modo}"
    
    # Suciedad en Fechas (múltiples formatos cronológicos)
    d = start_date + timedelta(days=int(np.random.uniform(0, 120)), minutes=int(np.random.uniform(300, 1380)))
    f_type = np.random.rand()
    if f_type < 0.40:
        fecha_str = d.strftime("%Y-%m-%d")
    elif f_type < 0.75:
        fecha_str = d.strftime("%d/%m/%Y")
    else:
        fecha_str = d.strftime("%Y/%m/%d")
    hora_str = d.strftime("%H:%M:%S")

    # Suciedad en Perfil de Usuario
    perf = np.random.choice(perfiles, p=[0.45, 0.25, 0.12, 0.05, 0.13])
    if np.random.rand() < 0.20:
        perf = perf.lower()

    # Suciedad en Tarifa_Pagada (caracteres no numéricos)
    tarifa_num = 3450 if perf == "Frecuente" else (1450 if perf == "Estudiantil" else 3600)
    t_noise = np.random.rand()
    if t_noise < 0.30:
        tarifa_str = f"${tarifa_num:,.0f}"
    elif t_noise < 0.60:
        tarifa_str = f"COP {tarifa_num}"
    elif t_noise < 0.85:
        tarifa_str = f"{tarifa_num}.00"
    else:
        tarifa_str = str(tarifa_num)

    # Transbordo e inconsistencias de texto / nulos
    es_transbordo = np.random.choice(["S", "N", "SI", "NO", "True", "False"], p=[0.15, 0.60, 0.10, 0.10, 0.02, 0.03])
    
    if es_transbordo in ["S", "SI", "True"]:
        t_trans = int(np.random.uniform(5, 55))
        minutos_transbordo = np.random.choice([f"{t_trans} min", str(t_trans), f"{t_trans}'"])
    else:
        minutos_transbordo = np.random.choice([None, "N/A", "0", "-"])

    medio = np.random.choice(medios_pago, p=[0.65, 0.25, 0.10])
    saldo_remanente = round(np.random.uniform(1200, 65000), 2)
    
    records.append({
        "ID_Validacion": id_val,
        "ID_Tarjeta": id_tarjeta,
        "Fecha_Lectura": fecha_str,
        "Hora_Lectura": hora_str,
        "Estacion_Parada": est_dirty,
        "Ruta_Modo_Transporte": ruta_modo_dirty,
        "Perfil_Usuario": perf,
        "Tarifa_Debitada": tarifa_str,
        "Es_Transbordo": es_transbordo,
        "Tiempo_Transbordo_Min": minutos_transbordo,
        "Medio_Acceso": medio,
        "Saldo_Posterior_Tarjeta": saldo_remanente
    })

df = pd.DataFrame(records)

# Agregar 60 registros duplicados para evaluar 'Quitar duplicados'
duplicated_rows = df.sample(n=60, random_state=42)
df_final = pd.concat([df, duplicated_rows], ignore_index=True)

# Guardar en archivo único
df_final.to_csv("Transporte_Metropolitano_Dirty.csv", index=False, encoding="utf-8-sig")
print(f"Dataset generado exitosamente: {len(df_final)} filas exportadas en 'Transporte_Metropolitano_Dirty.csv'.")