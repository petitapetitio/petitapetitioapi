# api.petitapetit.io

API de mon site personnel.


## How to install

Just type

```
python -m venv ~/dev/venvs/api.petitapetit.io_312
source ~/dev/venvs/api.petitapetit.io_312/bin/activate
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
2. log on the server (`pa`)
3. move to the project (`cd /var/www/petitapetitioapi/`)
4. `git pull` (with my user)
5. update the dependencies : `. ../venvs/petitapetitioapi_310/bin/activate; pip install -r requirements.txt`
6. `doas rcctl restart petitapetitioapi`
