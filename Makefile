GUNICORN := gunicorn app:app --workers=1 --threads=1

.PHONY: dev
dev:
	FLASK_ENV=development pipenv run flask run

.PHONY: prod
prod:
	pipenv run $(GUNICORN)

.PHONY: heroku
heroku:
	RUNNING_ON_HEROKU=1 $(GUNICORN)
