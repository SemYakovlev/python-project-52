install:
	uv pip install --system -r pyproject.toml

collectstatic:
	python manage.py collectstatic --no-input

migrate:
	python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi