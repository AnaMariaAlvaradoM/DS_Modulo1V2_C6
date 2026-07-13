import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check

np.random.seed(42)

SEDES = ["Chapinero", "Kennedy", "Suba", "Engativá"]
ESPECIALIDADES = ["Medicina General", "Odontología", "Pediatría", "Dermatología"]

# Cuántas de cada 10 citas acierta el modelo, por sede y versión
ACIERTOS = {
    "v1.0": {"Chapinero": 7, "Kennedy": 6, "Suba": 8, "Engativá": 7},
    "v1.1": {"Chapinero": 8, "Kennedy": 7, "Suba": 8, "Engativá": 8},
    "v2.0": {"Chapinero": 9, "Kennedy": 6, "Suba": 9, "Engativá": 8},
}

def version_de(noche):
    if noche <= 4: return "v1.0"
    if noche <= 8: return "v1.1"
    return "v2.0"

contador = [1000]
def simular_feed(noche):
    filas = []
    fecha = (pd.Timestamp("2026-06-01") + pd.Timedelta(days=noche-1)).strftime("%Y-%m-%d")
    version = version_de(noche)
    for sede in SEDES:
        k = ACIERTOS[version][sede]
        aciertos = np.array([True]*k + [False]*(10-k))
        np.random.shuffle(aciertos)
        for acierta in aciertos:
            asistio = bool(np.random.random() < 0.72)
            prediccion = (not asistio) if acierta else asistio
            prob = round(np.random.uniform(0.5, 0.97), 3) if prediccion else round(np.random.uniform(0.03, 0.5), 3)
            filas.append({
                "cita_id": f"CITA{contador[0]}", "fecha": fecha, "sede": sede,
                "especialidad": str(np.random.choice(ESPECIALIDADES)),
                "edad_paciente": int(np.random.randint(1, 90)),
                "prob_inasistencia": prob, "prediccion": bool(prediccion),
                "modelo_version": version, "asistio": asistio,
            })
            contador[0] += 1
    return pd.DataFrame(filas)

esquema = DataFrameSchema({
    "cita_id":           Column(str),
    "fecha":             Column(str),
    "sede":              Column(str, Check.isin(SEDES)),
    "especialidad":      Column(str),
    "edad_paciente":     Column(int, Check.in_range(0, 110)),
    "prob_inasistencia": Column(float, Check.in_range(0.0, 1.0), nullable=False),
    "prediccion":        Column(bool),
    "modelo_version":    Column(str),
    "asistio":           Column(bool),
})

engine = create_engine("sqlite:///healthcheck.db")

for noche in range(1, 13):
    feed = simular_feed(noche)
    feed_validado = esquema.validate(feed, lazy=True)
    feed_validado.to_sql("historial_predicciones", engine, if_exists="append", index=False)
    print(f"Noche {noche:2d} ({version_de(noche)}): {len(feed_validado)} citas validadas y acumuladas")

with engine.connect() as conn:
    total = conn.execute(text("SELECT COUNT(*) FROM historial_predicciones")).scalar()
print(f"\nHistorial total: {total} predicciones")