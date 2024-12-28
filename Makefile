
update:
	git pull
	@if [ -n "$(VIRTUAL_ENV)" ]; then \
		python -m pip install -r requirements.txt; \
	else \
		echo "Attention : l'environnement virtuel n'est pas activé. Les requirements n'ont pas été mis à jour"; \
	fi

devserver:
	python -m flask --app app run -h localhost -p 3000

restart:
	doas rcctl restart petitapetitioapid

stop:
	doas rcctl stop petitapetitioapid