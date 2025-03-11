build:
	docker build -t feature-requests .

run:
	$(MAKE) build
	docker run -p 8000:8000 feature-requests

cli:
	$(MAKE) build
	docker run -it feature-requests /bin/bash
