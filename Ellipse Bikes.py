import json
import folium
import requests

# Clé API
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

# URL de l'API
url = "https://api.jcdecaux.com/vls/v3/"

# Liste des villes à analyser
villes = ["nantes", "nancy", "dublin", "toulouse", "santander"]

# Fonction pour récupérer les données des vélos
def get_bike_data():
    bike_data = {}
    for ville in villes:
        ville_url = url + "stations?contract=" + ville + "&apiKey=" + api_key
        response = requests.get(ville_url)
        data = response.json()
        bike_data[ville] = data
    return bike_data


# Fonction pour afficher les données des vélos
def print_bike_data(bike_data):
    for ville, data in bike_data.items():
        nb_velos_electriques = sum([x['totalStands']['availabilities'].get('electricalBikes', 0) if 'totalStands' in x else 0 for x in data])
        nb_velos_mecaniques = sum([x['totalStands']['availabilities'].get('mechanicalBikes', 0) if 'totalStands' in x else 0 for x in data])
        nb_velos_total = nb_velos_electriques + nb_velos_mecaniques
        
        print(f"Pour la ville de {ville} :")
        print(f"Nombre de vélos total : {nb_velos_total}")
        print(f"Nombre de vélos électriques : {nb_velos_electriques}")
        print(f"Nombre de vélos mécaniques : {nb_velos_mecaniques}")
        print()
        
        if nb_velos_total == 0:
            pourcentage_velos_electriques = 0
            pourcentage_velos_mecaniques = 0
        else:
            pourcentage_velos_electriques = (nb_velos_electriques / nb_velos_total) * 100
            pourcentage_velos_mecaniques = (nb_velos_mecaniques / nb_velos_total) * 100
        
        print("Ville:", ville.capitalize())
        print("Nombre de vélos total:", nb_velos_total)
        print("Pourcentage de vélos électriques:", round(pourcentage_velos_electriques, 2), "%")
        print("Pourcentage de vélos mécaniques:", round(pourcentage_velos_mecaniques, 2), "%")
        print("-------------------------------")

# Création de la carte
map = folium.Map(location=[47.2184, -1.5536], zoom_start=12)

# Ajout des marqueurs pour chaque ville
bike_data = get_bike_data()
for ville, data in bike_data.items():
    for station in data:
        nom_station = station['name']
        latitude = station['position']['latitude']
        longitude = station['position']['longitude']
        nb_velos_electriques = station['totalStands']['availabilities']['electricalBikes'] if 'totalStands' in station else 0
        nb_velos_mecaniques = station['totalStands']['availabilities']['mechanicalBikes'] if 'totalStands' in station else 0
        html = f"<b>Station:</b> {nom_station}<br><b>Vélos électriques:</b> {nb_velos_electriques}<br><b>Vélos mécaniques:</b> {nb_velos_mecaniques}"
        popup = folium.Popup(html, max_width=300)
        folium.Marker([latitude, longitude], popup=popup).add_to(map)

# Sauvegarde de la carte
map.save("stations_velos.html")

# Fonction pour mettre à jour la carte
def update_map(m, bike_data):
    # À implémenter
    pass

# Fonction principale
def main():
    # Afficher les données des vélos
    print_bike_data(bike_data)
    
    # Mettre à jour la carte
  
    update_map(map, bike_data)  # Appel à la fonction update_map()

# Exécution du programme
if __name__ == "__main__":
    main()
