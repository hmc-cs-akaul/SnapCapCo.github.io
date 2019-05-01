.PHONY: dev
dev:
	FLASK_ENV=development pipenv run flask run

.PHONY: prod
prod:
	pipenv run gunicorn app:app --workers=1 --threads=1

.PHONY: heroku
heroku:
	pip install fastai==1.0.52 --no-deps
	make prod
