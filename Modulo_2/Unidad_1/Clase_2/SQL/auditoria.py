from sqlalchemy import select, func
from sqlalchemy.orm import Session
from Unidad_1.Clase_2.SQL.modelos_db import engine, PrediccionCancelacion

with Session(engine) as session:
    total = session.scalar(select(func.count()).select_from(PrediccionCancelacion))
    print("Total de predicciones guardadas:", total)

    alto = session.scalars(
        select(PrediccionCancelacion).where(PrediccionCancelacion.prob_cancelacion >= 0.8)
    ).all()
    print("Pedidos de alto riesgo (prob >= 0.8):", len(alto))

    prom = session.scalar(select(func.avg(PrediccionCancelacion.prob_cancelacion)))
    print("Probabilidad promedio de cancelación:", round(prom, 4))

with Session(engine) as session:
    consulta = (
        select(PrediccionCancelacion.categoria, func.count())
        .where(PrediccionCancelacion.prediccion == True)
        .group_by(PrediccionCancelacion.categoria)
        .order_by(func.count().desc())
    )
    print("Cancelaciones predichas por categoría:")
    for categoria, cantidad in session.execute(consulta).all():
        print(f"  {categoria}: {cantidad}")