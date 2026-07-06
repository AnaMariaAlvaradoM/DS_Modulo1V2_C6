import pandas as pd
import numpy as np

np.random.seed(42)

N = 200
categorias = ["Pasta", "Pizza", "Sushi", "Burgers", "Postres", "Bebidas", "Ensaladas"]
ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla"]

df = pd.DataFrame({
    "pedido_id": [f"PED{1000+i}" for i in range(N)],
    "restaurante_id": np.random.randint(1, 51, size=N),
    "categoria": np.random.choice(categorias, size=N),
    "ciudad": np.random.choice(ciudades, size=N),
    "precio": np.round(np.random.uniform(8000, 65000, size=N), 0),
    "calificacion": np.round(np.random.uniform(3.0, 5.0, size=N), 1),
})
df.to_csv("feed_sano.csv", index=False)

dfc = df.copy()
dfc["precio"] = dfc["precio"].astype(object)
idx_texto = dfc.sample(40, random_state=1).index
dfc.loc[idx_texto, "precio"] = dfc.loc[idx_texto, "precio"].apply(
    lambda x: f"${int(x):,}".replace(",", "."))
idx_nulos = dfc.sample(15, random_state=2).index
dfc.loc[idx_nulos, "calificacion"] = np.nan
idx_rango = dfc.sample(8, random_state=3).index
dfc.loc[idx_rango, "calificacion"] = np.round(np.random.uniform(6, 10, size=8), 1)
dfc = dfc.rename(columns={"ciudad": "city"})
dfc.to_csv("feed_corrupto.csv", index=False)

print("Feeds generados: feed_sano.csv y feed_corrupto.csv")