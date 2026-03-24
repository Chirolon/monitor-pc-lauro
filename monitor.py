import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import time

# --- TUS COMPONENTES (Hard Gamers ARG) ---
PRODUCTOS = [
    {"nombre": "CPU: Ryzen 5 9600X", "url": "https://www.hardgamers.com.ar/search?text=Ryzen+5+9600X"},
    {"nombre": "GPU: RX 9060 XT 16GB", "url": "https://www.hardgamers.com.ar/search?text=RX+9060+XT+16GB"},
    {"nombre": "Mother: Gigabyte B650E EAGLE", "url": "https://www.hardgamers.com.ar/search?text=Gigabyte+B650E+EAGLE"},
    {"nombre": "RAM: Crucial Pro 32GB DDR5 6000", "url": "https://www.hardgamers.com.ar/search?text=Crucial+Pro+32GB+6000MHz"},
    {"nombre": "SSD: WD Black SN7100 1TB", "url": "https://www.hardgamers.com.ar/search?text=WD+Black+SN7100+1TB"},
    {"nombre": "Fuente: XPG Core Reactor II 850W", "url": "https://www.hardgamers.com.ar/search?text=XPG+Core+Reactor+II+850W"},
    {"nombre": "Cooler: MasterLiquid 240 Core", "url": "https://www.hardgamers.com.ar/search?text=MasterLiquid+240+Core"}
]

def obtener_precio(url):
    try:
        # Esto engaña a la web para que crea que sos vos desde tu ASUS
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            return "Error Acceso"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscamos el precio en la estructura de Hard Gamers
        precio_tag = soup.find('h2', class_='product-price')
        if precio_tag:
            # Limpia el texto para dejar solo el número
            precio_texto = precio_tag.text.strip().replace('$', '').replace('.', '').replace(',', '').split()[0]
            return precio_texto
        
        return "Sin Stock"
    except Exception as e:
        return f"Error: {str(e)[:20]}"

def actualizar_excel():
    fecha = datetime.now().strftime("%d/%m/%Y")
    archivo = 'presupuesto_pc_lauro.csv'
    existe = os.path.isfile(archivo)
    
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Si el archivo es nuevo, pone los títulos
        if not existe:
            writer.writerow(['Fecha', 'Componente', 'Precio ARS'])
        
        for p in PRODUCTOS:
            precio = obtener_precio(p['url'])
            writer.writerow([fecha, p['nombre'], precio])
            print(
