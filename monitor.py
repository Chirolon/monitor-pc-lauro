name: Monitor de Precios Lauro
on:
  schedule:
    # Esto corre todos los días a las 13:00 UTC (10:00 AM de Argentina)
    - cron: '0 13 * * *' 
  workflow_dispatch:      # Este añade el botón "Run workflow" para que lo pruebes CUANDO QUIERAS

jobs:
  track-prices:
    runs-on: ubuntu-latest
    permissions:
      contents: write    # ESTO ES CLAVE: Permite que el bot escriba en tu Excel
    steps:
      - name: Clonar el repositorio
        uses: actions/checkout@v3

      - name: Instalar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Instalar librerías necesarias
        run: pip install requests beautifulsoup4

      - name: Ejecutar el script de monitoreo
        run: python monitor.py

      - name: Guardar cambios en el Excel
        run: |
          git config --global user.name 'PC-Price-Bot'
          git config --global user.email 'bot@github.com'
          git add presupuesto_pc_lauro.csv
          git commit -m "Update precios build $(date +'%d/%m/%Y')" || exit 0
          git push
