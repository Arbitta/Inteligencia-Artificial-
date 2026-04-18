import pandas as pd
import matplotlib.pyplot as plt

#df = pd.read_csv(results.csv)
df = pd.read_csv(r'd:/Users/Usuario/Desktop/Inteligencia Artificial/Lab1/punto 3/results.csv')
#print(df)
# ───────────────────── Cargar los datos ─────────────────────────────────────
print("EXPLORACIÓN INICIAL DEL DATASET")

print("\nPrimeras 5 filas:")
print(df.head())

# Dimensiones
print(f"\nDimensiones del dataset: {df.shape[0]} filas × {df.shape[1]} columnas")

# Tipos de datos
print("\nTipos de datos:")
print(df.dtypes)


# ─────────────────────LIMPIEZA DE DATOS ─────────────────────────────────────

df['date'] = pd.to_datetime(df['date'])
df = df.dropna()# Elimina filas con valores nulos
df['year'] = df['date'].dt.year # Agregar columna de año

# Agregar columna con el resultado de quien gano
def resultado(row):
    if row['home_score'] > row['away_score']:
        return 'Local'
    elif row['home_score'] < row['away_score']:
        return 'Visitante'
    else:
        return 'Empate'

df['resultado'] = df.apply(resultado, axis=1)

print("DATASET MODIFICADO")
print(df.head())

# ──  FILTRADO ───────────────────────────────────────────────
# Filtrar solo partidos de Argentina
argentina = df[(df['home_team'] == 'Argentina') | (df['away_team'] == 'Argentina')].copy()
print(f"\nPartidos de Argentina: {len(argentina)}")

# ── ANÁLISIS ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("ANÁLISIS DE DATOS")
print("=" * 50)


# Promedio de goles por partido
df['total_goles'] = df['home_score'] + df['away_score']
print(f"\nPromedio de goles por partido: {df['total_goles'].mean():.2f}")

# Años con más partidos jugados
print("\nTop 5 años con más partidos:")
print(df.groupby('year').size().sort_values(ascending=False).head())

# Selecciones con más partidos
todas = pd.concat([df['home_team'], df['away_team']])
print("\nTop 10 selecciones con más partidos:")
print(todas.value_counts().head(10))

# ──  GRÁFICOS ───────────────────────────────────────────────

#  Distribución de resultado
resultados_conteo = df['resultado'].value_counts()
colores = ['#4C8BBF', '#E07B4C', '#6CB87A']

plt.figure(figsize=(7, 7))
plt.pie(
    resultados_conteo,
    labels=resultados_conteo.index,
    autopct='%1.1f%%',
    colors=colores,
    startangle=140,
)
plt.title('Distribución de resultados en partidos internacionales', fontsize=14, pad=20)
plt.tight_layout()
plt.show()


# Gráfico 2: Top 10 selecciones con más partidos
top_selecciones = todas.value_counts().head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_selecciones.index[::-1], top_selecciones.values[::-1], color='#6CB87A')
plt.title('Top 10 selecciones con más partidos internacionales', fontsize=14)
plt.xlabel('Cantidad de partidos')
plt.show()

print("\n¡Análisis completado! Gráficos guardados.")