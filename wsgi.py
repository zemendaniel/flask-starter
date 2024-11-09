import sys
import os

# Az alkalmazás könyvtárát hozzáadjuk a sys.path-hez
# Állítsd be az abszolút elérési utat az alkalmazás könyvtárához
sys.path.insert(0, '/~/flask-starter')

# Aktiváljuk a virtuális környezetet
activate_this = 'venv/bin/activate'


# Aktiváljuk a virtuális környezetet
os.environ['VIRTUAL_ENV'] = '~/flask-starter/venv'
os.environ['PATH'] = '~/flask-starter/venv/bin:' + os.environ['PATH']
os.environ['PYTHONHOME'] = '~/flask-starter/venv'
from app import create_app


application = create_app()