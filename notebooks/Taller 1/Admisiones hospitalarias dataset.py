from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Semilla fija para reproducibilidad
np.random.seed(42)
n_admissions = 1000

# 1. Catálogo base de Diagnósticos
diagnoses_pool = [
    ("DX-01", "Infarto Agudo de Miocardio", "Cardiología", "Alta"),
    ("DX-02", "Insuficiencia Cardíaca Congestiva", "Cardiología", "Alta"),
    ("DX-03", "Neumonía Bacteriana", "Neumología", "Media"),
    ("DX-04", "Crisis Asmática Severa", "Neumología", "Baja"),
    ("DX-05", "Apendicitis Aguda", "Cirugía General", "Media"),
    ("DX-06", "Colecistitis Aguda", "Cirugía General", "Media"),
    ("DX-07", "Traumatismo Craneoencefálico", "Neurología", "Alta"),
    ("DX-08", "Accidente Cerebrovascular", "Neurología", "Alta"),
    ("DX-09", "Cetoacidosis Diabética", "Endocrinología", "Media"),
    ("DX-10", "Gastroenteritis Severa", "Medicina Interna", "Baja"),
]

# 2. Catálogo base de Servicios / Unidades
services_pool = [
    ("SRV-01", "Urgencias Generales", "Piso 1", 45),
    ("SRV-02", "Unidad de Cuidados Intensivos (UCI)", "Piso 3", 18),
    ("SRV-03", "Cirugía y Recuperación", "Piso 2", 25),
    ("SRV-04", "Medicina Interna", "Piso 4", 50),
    ("SRV-05", "Trauma Shock", "Piso 1", 12),
]

# 3. Catálogo base de Pacientes (350 pacientes recurrentes para generar granularidad 1:N)
n_patients = 350
patient_ids = [f"PAC-{1000 + i}" for i in range(n_patients)]
genders = np.random.choice(["Femenino", "Masculino"], size=n_patients, p=[0.52, 0.48])
blood_types = np.random.choice(
    ["O+", "O-", "A+", "A-", "B+", "AB+"],
    size=n_patients,
    p=[0.55, 0.08, 0.25, 0.04, 0.06, 0.02],
)
ages = np.random.randint(18, 88, size=n_patients)
cities = np.random.choice(
    ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga"],
    size=n_patients,
    p=[0.35, 0.25, 0.18, 0.12, 0.10],
)

patients_dict = {
    pid: {"Edad": a, "Genero": g, "Grupo_Sanguineo": bt, "Ciudad_Residencia": c}
    for pid, a, g, bt, c in zip(patient_ids, ages, genders, blood_types, cities)
}

# 4. Generación de las 1.000 filas desnormalizadas
start_date = datetime(2025, 1, 1)
records = []

for i in range(1, n_admissions + 1):
    id_adm = f"ADM-{20250000 + i}"

    # Asignación de entidades
    pid = np.random.choice(patient_ids)
    p_info = patients_dict[pid]

    dx = diagnoses_pool[np.random.choice(len(diagnoses_pool))]
    srv = services_pool[
        np.random.choice(len(services_pool), p=[0.38, 0.15, 0.15, 0.22, 0.10])
    ]

    adm_date = start_date + timedelta(days=int(np.random.uniform(0, 365)))
    los = int(np.random.poisson(lam=4)) + 1
    dis_date = adm_date + timedelta(days=los)

    wait_time = int(np.random.exponential(scale=45)) + 8

    # Costos coherentes con severidad y estancia
    base_cost = 3500000 if srv[0] == "SRV-02" else 850000
    daily_rate = 1250000 if srv[0] == "SRV-02" else 380000
    total_cost = round(
        base_cost + (daily_rate * los) + np.random.normal(150000, 30000), 2
    )

    ins = np.random.choice(
        ["Contributivo", "Subsidiado", "Póliza Privada"], p=[0.50, 0.35, 0.15]
    )
    adm_type = np.random.choice(
        ["Urgencias", "Programada", "Remitido"], p=[0.65, 0.20, 0.15]
    )
    readm = np.random.choice(["Sí", "No"], p=[0.14, 0.86])

    records.append(
        {
            # Evento (Hechos)
            "ID_Admision": id_adm,
            "Fecha_Ingreso": adm_date.strftime("%Y-%m-%d"),
            "Fecha_Alta": dis_date.strftime("%Y-%m-%d"),
            "Tipo_Ingreso": adm_type,
            "Tipo_Aseguradora": ins,
            "Tiempo_Espera_Minutos": wait_time,
            "Dias_Estancia": los,
            "Costo_Total_Facturado": total_cost,
            "Reingreso_30_Dias": readm,
            # Atributos del Paciente (Dim_Paciente)
            "ID_Paciente": pid,
            "Edad_Paciente": p_info["Edad"],
            "Genero_Paciente": p_info["Genero"],
            "Grupo_Sanguineo": p_info["Grupo_Sanguineo"],
            "Ciudad_Paciente": p_info["Ciudad_Residencia"],
            # Atributos del Diagnóstico (Dim_Diagnostico)
            "Codigo_Diagnostico": dx[0],
            "Nombre_Diagnostico": dx[1],
            "Especialidad_Medica": dx[2],
            "Severidad_Diagnostico": dx[3],
            # Atributos del Servicio (Dim_Servicio)
            "Codigo_Servicio": srv[0],
            "Nombre_Servicio": srv[1],
            "Ubicacion_Servicio": srv[2],
            "Capacidad_Camas": srv[3],
        }
    )

df_flat = pd.DataFrame(records)

# Guardar en archivo único
df_flat.to_csv("Hospital_Admissions_Flat.csv", index=False, encoding="utf-8-sig")
print(
    f"Archivo exportado: 'Hospital_Admissions_Flat.csv' con {len(df_flat)} filas y {len(df_flat.columns)} columnas."
)
