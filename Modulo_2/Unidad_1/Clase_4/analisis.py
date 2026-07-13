from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///healthcheck.db")

def consultar(sql, titulo):
    print(f"\n{titulo}")
    with engine.connect() as conn:
        for fila in conn.execute(text(sql)):
            print("  ", tuple(fila))

consultar("""
    SELECT ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END), 3) AS tasa_acierto,
           COUNT(*) AS total
    FROM historial_predicciones
""", "Tasa de acierto global:")

consultar("""
    SELECT modelo_version,
           ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END), 3) AS tasa_acierto,
           COUNT(*) AS predicciones
    FROM historial_predicciones
    GROUP BY modelo_version
    ORDER BY modelo_version
""", "Tasa de acierto por versión:")


consultar("""
    SELECT sede,
           ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END), 3) AS tasa
    FROM historial_predicciones
    GROUP BY sede
    HAVING AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END) >= 0.75
    ORDER BY tasa DESC
""", "Sedes confiables (tasa >= 0.75):")


consultar("""
    SELECT sede, modelo_version,
           ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END), 3) AS tasa
    FROM historial_predicciones
    GROUP BY sede, modelo_version
    ORDER BY sede, modelo_version
""", "Tasa por sede y versión:")



consultar("""
    SELECT sede, modelo_version,
           ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END), 3) AS tasa,
           ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END)
                 - LAG(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END))
                   OVER (PARTITION BY sede ORDER BY modelo_version), 3) AS cambio
    FROM historial_predicciones
    GROUP BY sede, modelo_version
    ORDER BY sede, modelo_version
""", "Cambio de tasa: cada versión contra la anterior:")


consultar("""
    SELECT sede, cita_id, prob_inasistencia FROM (
        SELECT sede, cita_id, prob_inasistencia,
               ROW_NUMBER() OVER (PARTITION BY sede ORDER BY prob_inasistencia DESC) AS puesto
        FROM historial_predicciones
        WHERE fecha = '2026-06-12'
    ) WHERE puesto <= 3
    ORDER BY sede, prob_inasistencia DESC
""", "Top 3 de riesgo por sede (última jornada):")



consultar("""
    SELECT especialidad,
           ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END), 3) AS tasa,
           COUNT(*) AS citas,
           RANK() OVER (ORDER BY AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END) DESC) AS puesto
    FROM historial_predicciones
    GROUP BY especialidad
    ORDER BY puesto
""", "Podio del modelo por especialidad:")


with engine.connect() as conn:
    conn.execute(text("DROP VIEW IF EXISTS reporte_rendimiento"))
    conn.execute(text("""
        CREATE VIEW reporte_rendimiento AS
        SELECT modelo_version, sede,
               ROUND(AVG(CASE WHEN prediccion <> asistio THEN 1.0 ELSE 0.0 END), 3) AS tasa_acierto,
               COUNT(*) AS predicciones
        FROM historial_predicciones
        GROUP BY modelo_version, sede
    """))
    conn.commit()

consultar("""
    SELECT * FROM reporte_rendimiento
    WHERE modelo_version = 'v2.0'
    ORDER BY tasa_acierto DESC
""", "La directora consulta su reporte (v2.0):")