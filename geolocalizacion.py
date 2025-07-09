import requests

API_KEY = '80bfef64-dc82-406f-bc6f-cff462832511'

def obtener_coordenadas(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json()["hits"]:
        punto = response.json()["hits"][0]
        return f'{punto["point"]["lat"]},{punto["point"]["lng"]}'
    else:
        return None

def obtener_datos(origen, destino, modo):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [origen, destino],
        "vehicle": modo,
        "locale": "es",
        "calc_points": True,
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        distancia_m = data['paths'][0]['distance']
        duracion_s = data['paths'][0]['time'] / 1000
        instrucciones = data['paths'][0]['instructions']

        distancia_km = round(distancia_m / 1000, 2)
        distancia_millas = round(distancia_km * 0.621371, 2)
        duracion_min = round(duracion_s / 60, 2)

        print(f"\n📍 Distancia: {distancia_km} km / {distancia_millas} millas")
        print(f"⏱️ Duración estimada: {duracion_min} minutos")
        print("\n🧭 Narrativa del viaje:")
        for paso in instrucciones:
            print(f"- {paso['text']}")
    else:
        print("❌ Error al consultar la API:", response.status_code)
        print(response.text)

def main():
    while True:
        print("\n🗺️ Calculador de rutas entre ciudades")
        salida = input("Presiona 's' para salir o Enter para continuar: ").lower()
        if salida == 's':
            break

        origen_texto = input("Ciudad de origen (Ej: Santiago, Chile): ")
        destino_texto = input("Ciudad de destino (Ej: Buenos Aires, Argentina): ")

        origen_coords = obtener_coordenadas(origen_texto)
        destino_coords = obtener_coordenadas(destino_texto)

        if not origen_coords or not destino_coords:
            print("❌ No se pudo geocodificar alguna de las ciudades.")
            continue

        print("Modos de transporte disponibles:")
        print("1. car")
        print("2. bike")
        print("3. foot")
        modo_input = input("Elige el modo (escribe: car, bike o foot): ")

        if modo_input not in ['car', 'bike', 'foot']:
            print("⚠️ Modo inválido.")
            continue

        obtener_datos(origen_coords, destino_coords, modo_input)

if __name__ == "__main__":
    main()
