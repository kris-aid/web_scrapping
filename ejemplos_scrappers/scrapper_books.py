import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. Configuración
URL = "http://books.toscrape.com/"
print(f"Iniciando el scraping en: {URL}...")
# Lista para almacenar todos los libros de todas las páginas
todos_los_libros = []


for pagina in range(1, 6):
    # Construimos la URL dinámica para cada página
    url = f"http://books.toscrape.com/catalogue/page-{pagina}.html"
    print(f"🔎 Analizando página {pagina}...")
    
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        libros = soup.find_all('article', class_='product_pod')
        
        for libro in libros:
            # 1. Título completo (del atributo 'title')
            titulo = libro.h3.a['title']
            
            # 2. Precio
            precio = libro.find('p', class_='price_color').text.strip()
            
            # 3. Estrellas (están en la clase de la etiqueta <p>)
            # La clase es algo como ['star-rating', 'Three']
            clases_estrellas = libro.find('p', class_='star-rating')['class']
            estrellas = clases_estrellas[1] # Tomamos la segunda palabra (Three, Two, etc.)
            
            # 4. Disponibilidad
            stock = libro.find('p', class_='instock availability').text.strip()
            
            # Guardamos la info del libro
            todos_los_libros.append({
                "Título": titulo,
                "Precio": precio,
                "Estrellas": estrellas,
                "Disponibilidad": stock,
                "Página": pagina
            })
        
        # Buena práctica: esperar un segundo entre páginas para no saturar el servidor
        time.sleep(1)
    else:
        print(f"⚠️ Error en página {pagina}: Código {respuesta.status_code}")

# Convertir a DataFrame y guardar
df_final = pd.DataFrame(todos_los_libros)
df_final.to_csv("libros_completos.csv", index=False)

print(f"\n✅ ¡Proceso terminado! Se extrajeron {len(df_final)} libros en total.")
print("El archivo 'libros_completos.csv' ya está listo.")