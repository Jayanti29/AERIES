.PHONY: help build run test lint clean docker-up docker-down

help:
	@echo "AERIS - Operational Decision-Support & Simulation Platform"
	@echo "Targets:"
	@echo "  build       Build backend and frontend"
	@echo "  docker-up   Start all services via Docker Compose"
	@echo "  docker-down Stop all services"
	@echo "  test        Run backend tests and verification suite"
	@echo "  lint        Run code linters"
	@echo "  clean       Remove temporary and cache files"

build:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install && npm run build

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v

test:
	python3 -m unittest discover -s tests -p "test_*.py"

lint:
	python3 -m ruff check backend/ || true

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/dist
