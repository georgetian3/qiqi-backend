set -e
python3.11 -m venv .venv
source .venv/bin/activate
python3 -m pip install --no-cache-dir --index-url=https://pypi.org/simple/ -r requirements.txt
python3 main.py --reset