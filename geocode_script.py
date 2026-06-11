import pandas as pd
import requests
import re
import time

input_file = 'Adresses.xlsx'
df = pd.read_excel(input_file, sheet_name='Feuil1')

def geocode_address(address):
    if not isinstance(address, str):
        return None, None
    clean_addr = re.sub(r'\s*[-–]\s*[^,]+', '', address)
    
    url = 'https://api-adresse.data.gouv.fr/search/'
    params = {'q': clean_addr, 'limit': 1}
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['features']:
                coords = data['features'][0]['geometry']['coordinates']
                return coords[1], coords[0]  # latitude, longitude
    except Exception as e:
        pass
    return None, None

lats = []
lons = []

print("Starting geocoding of addresses...")
for idx, row in df.iterrows():
    lat, lon = geocode_address(row['adresse_rue'])
    lats.append(lat)
    lons.append(lon)
    if idx > 0 and idx % 100 == 0:
        print(f"Processed {idx} addresses...")
    time.sleep(0.05) # 20 requests per second to respect rate limit

df['latitude'] = lats
df['longitude'] = lons

df.to_excel(input_file, sheet_name='Feuil1', index=False)
print(f"Geocoding complete! Found coordinates for {len([l for l in lats if l is not None])} addresses. Saved to {input_file}")
