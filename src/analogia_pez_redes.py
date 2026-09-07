import numpy as np
import matplotlib.pyplot as plt

# Configuración de reproducibilidad
np.random.seed(42)

# Parámetros del experimento
mu_real = 50.0       # Parámetro poblacional fijo (el pez)
sigma = 10.0         # Desviación estándar poblacional
n = 30               # Tamaño de cada muestra
n_muestras = 25      # Número de muestras independientes (redes)
z_critico = 1.96     # Nivel de confianza del 95%

# Error estándar teórico
se = sigma / np.sqrt(n)

# Generación de intervalos
medias = []
intervalos = []
capturas = []

for _ in range(n_muestras):
    muestra = np.random.normal(loc=mu_real, scale=sigma, size=n)
    x_barra = np.mean(muestra)
    # Error estándar estimado con la desviación muestral (s)
    s = np.std(muestra, ddof=1)
    margen_error = z_critico * (s / np.sqrt(n))
    
    lim_inf = x_barra - margen_error
    lim_sup = x_barra + margen_error
    
    # Comprobar si la red capturó el pez
    exito = (lim_inf <= mu_real <= lim_sup)
    
    medias.append(x_barra)
    intervalos.append((lim_inf, lim_sup))
    capturas.append(exito)

# Configuración gráfica
plt.figure(figsize=(9, 7), dpi=150)

# Línea vertical del parámetro real fijo (el pez inmóvil)
plt.axvline(x=mu_real, color='#15803d', linestyle='-', linewidth=2, 
            label=r'Parámetro poblacional real fijo ($\mu = 50$)', zorder=2)

# Trazado de cada intervalo (red)
for i in range(n_muestras):
    x_barra = medias[i]
    inf, sup = intervalos[i]
    exito = capturas[i]
    
    color = '#1d4ed8' if exito else '#b91c1c'
    label_punto = None
    
    # Segmento horizontal (la red)
    plt.plot([inf, sup], [i + 1, i + 1], color=color, linewidth=1.8, zorder=3)
    
    # Punto central (la estimación puntual / posición de la barca)
    plt.scatter(x_barra, i + 1, color=color, s=25, zorder=4)

# Formato y anotaciones pedagógicas
plt.title("Analogía de la pesca: 25 Intervalos de Confianza al 95%", fontsize=13, pad=15)
plt.xlabel("Escala de la variable medida", fontsize=11)
plt.ylabel("Muestra independiente (Lanzamiento de red)", fontsize=11)
plt.yticks(range(1, n_muestras + 1, 2))
plt.grid(axis='x', linestyle=':', alpha=0.6)

# Leyenda explicativa
plt.plot([], [], color='#1d4ed8', marker='o', label='Red exitosa (captura a $\mu$)', linestyle='-')
plt.plot([], [], color='#b91c1c', marker='o', label='Red fallida (no contiene a $\mu$)', linestyle='-')
plt.legend(loc='upper right', frameon=True, framealpha=0.9)

plt.tight_layout()
plt.show()