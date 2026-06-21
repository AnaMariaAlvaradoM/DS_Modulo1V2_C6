import random
from datetime import datetime
from sqlalchemy.orm import Session
from Unidad_1.Clase_2.SQL.modelos_db import engine, PrediccionCancelacion

random.seed(42)

categorias = ["Chicken", "Beef", "Side", "Pasta", "Seafood", "Dessert", "Vegetarian"]

predicciones = []
for i in range(500):
    prob = round(random.uniform(0, 1), 3)
    predicciones.append({
        "id_pedido": f"PED{1000 + i}",
        "categoria": random.choice(categorias),
        "valor_pedido": round(random.uniform(15000, 95000), 0),
        "prob_cancelacion": prob,
        "prediccion": prob >= 0.5,
        "modelo_version": "v1.0",
    })

print("Predicciones generadas:", len(predicciones))


ahora = datetime.now()

with Session(engine) as session:
    objetos = [PrediccionCancelacion(creado_en=ahora, **p) for p in predicciones]
    session.add_all(objetos)
    session.commit()
    print("Predicciones guardadas y confirmadas:", len(objetos))