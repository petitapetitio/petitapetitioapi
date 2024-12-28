# api.petitapetit.io

API de mon site personnel.


## How to install

Just type

```
python -m venv .venv
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install --upgrade setuptools
python -m pip install -r requirements.txt
```

then

```
flask --app app run
```

## How to update the website 

1. push the changes
2. log on the server (pa) and pull (with my user)
3. `doas rcctl restart leequotesd`
