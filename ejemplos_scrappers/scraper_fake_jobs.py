import pandas as pd
from bs4 import BeautifulSoup
import requests
# Definimos la URL de nuestro caso de estudio
URL = "https://realpython.github.io/fake-jobs/"

# Realizamos la petición GET
respuesta = requests.get(URL)

# Verificamos qué nos respondió el servidor
print(f"Código de estado: {respuesta.status_code}") # 200 significa éxito
# 1. Tomamos el contenido de la respuesta que obtuvimos con requests
# 2. "Cocinamos" el HTML para crear nuestro objeto 'soup'
soup = BeautifulSoup(respuesta.text, 'html.parser')

# Ahora 'soup' es un objeto que representa toda la estructura de la página
print("¡Objeto BeautifulSoup creado con éxito!")


ofertas = soup.find_all("div", class_="card-content")

print(f"Procesando {len(ofertas)} ofertas...\n")

# 1. Creamos una lista vacía para guardar nuestros diccionarios
datos_finales = []

# 2. Iteramos (repetimos) sobre todas las ofertas que encontramos
for oferta in ofertas:
    info = {
        "Puesto": oferta.find("h2", class_="title").text.strip(),
        "Empresa": oferta.find("h3", class_="company").text.strip(),
        "Ubicación": oferta.find("p", class_="location").text.strip(),
        # aquí añadan el como encontraron su fecha c: ( no se olviden de terminar la linea con una coma)
        "Link": oferta.find_all("a")[1]["href"]
    }
    datos_finales.append(info)

# 3. Convertimos la lista en un DataFrame (una tabla)
df = pd.DataFrame(datos_finales)

# 4. Guardamos la tabla en un archivo .csv
df.to_csv("ofertas_trabajo.csv", index=False)
print("¡Archivo 'ofertas_trabajo.csv' creado con éxito!")

