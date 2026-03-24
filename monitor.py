import cloudscraper
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
import time

# --- COMPONENTES ---
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
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, timeout=20)
        if response.status_code != 200:
            return "Bloqueado"
        soup = BeautifulSoup(response.content, 'html.parser')
        precio_tag = soup.find('h2', class_='product-price')
        if precio_tag:
            return precio_tag.text.strip().replace('$', '').replace('.', '').replace(',', '').split()[0]
        return "Sin Stock"
    except Exception:
        return "Error"

def actualizar_excel():
    fecha = datetime.now().strftime("%d/%m/%Y")
    archivo = 'presupuesto_pc_lauro.csv'
    existe = os.path.isfile(archivo)
    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(['Fecha', 'Componente', 'Precio ARS'])
        for p in PRODUCTOS:
            precio = obtener_precio(p['url'])
            writer.writerow([fecha, p['nombre'], precio])
            print(f"{p['nombre']}: {precio}")
            time.sleep(5)

if __name__ == "__main__":
    actualizar_excel()
