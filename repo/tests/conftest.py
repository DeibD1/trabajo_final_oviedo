# repo/tests/conftest.py
import sys
import os

# Calculamos la ruta absoluta a repo/src desde la ubicación de este conftest.py
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)