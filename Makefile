prepare:
	poetry shell

install-deps:
	poetry install

run-tests:
	poetry run pytest tests/ -v

run-app:
	poetry run uvicorn app.main:app --port 8081 --reload

build-emulators:
	@docker build \
		--tag google_cloud:emulators \
		-f Dockerfile.emulators \
		.

run-emulators:
	@docker run --rm -d \
		--name google_cloud_emulators \
		--publish 8085:8085 \
		--publish 8086:8086 \
		google_cloud:emulators
