from pymongo import MongoClient

# Reemplazar por la URI real de Atlas
client = MongoClient("mongodb+srv://masterIA:wYDxdbN9pi8PVGL1@cluster0.ixndx1o.mongodb.net/?appName=Cluster0")

db = client["rappi_ml"]          # base de datos
coleccion = db["modelos"]        # colección (se crea sola al primer insert)

print("Conexión lista. Colecciones:", db.list_collection_names())


from datetime import datetime

modelo_v1 = {
    "nombre": "predictor_cancelaciones",
    "version": "v1.0",
    "algoritmo": "RandomForest",
    "metricas": {"accuracy": 0.87, "precision": 0.83, "recall": 0.79},
    "features": ["categoria", "valor_pedido", "hora", "ciudad"],
    "entrenado_en": datetime(2026, 6, 15),
    "notas": "Primer modelo en producción. Falta validar en Medellín.",
}
resultado = coleccion.insert_one(modelo_v1)
print("Documento insertado. _id generado:", resultado.inserted_id)

modelo_v2 = {
    "nombre": "predictor_cancelaciones",
    "version": "v2.0",
    "algoritmo": "XGBoost",
    "metricas": {"accuracy": 0.91, "precision": 0.88, "recall": 0.85, "f1": 0.86},
    "features": ["categoria", "valor_pedido", "hora", "ciudad", "clima", "dia_semana"],
    "hiperparametros": {"max_depth": 6, "learning_rate": 0.1},  # campo nuevo
    "entrenado_en": datetime(2026, 6, 18),
}
coleccion.insert_one(modelo_v2)
print("v2.0 insertado con campos nuevos, sin alterar esquema.")

total = coleccion.count_documents({})
print("Documentos en la colección:", total)

v2 = coleccion.find_one({"version": "v2.0"})
print("v2.0 accuracy:", v2["metricas"]["accuracy"])

buenos = coleccion.count_documents({"metricas.accuracy": {"$gte": 0.90}})
print("Modelos con accuracy >= 0.90:", buenos)

# UPDATE: marcar v2.0 como modelo en producción
coleccion.update_one(
    {"version": "v2.0"},
    {"$set": {"estado": "produccion"}}
)

# DELETE: dar de baja el modelo viejo v1.0
coleccion.delete_one({"version": "v1.0"})
print("Documentos tras eliminar v1.0:", coleccion.count_documents({}))