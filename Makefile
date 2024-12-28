
update:
	git pull
	python -m pip install -r requirements.txt

devserver:
	python -m flask --app app run

restart:
	doas rcctl restart petitapetitioapid