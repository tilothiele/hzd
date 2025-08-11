# Makefile for HZD Antragsformular Docker Image

# Variables
IMAGE_NAME = hzd-antragsformular
BRANCH_NAME = $(shell git rev-parse --abbrev-ref HEAD)
COMMIT_HASH = $(shell git rev-parse --short HEAD)
IMAGE_TAG = snapshot-$(BRANCH_NAME)-$(COMMIT_HASH)
FULL_IMAGE_NAME = tilothiele/$(IMAGE_NAME):$(IMAGE_TAG)
CONTAINER_NAME = hzd-antragsformular-container
PORT = 3000

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build     - Build Docker image"
	@echo "  run       - Run container"
	@echo "  stop      - Stop container"
	@echo "  clean     - Remove container and image"
	@echo "  logs      - Show container logs"
	@echo "  shell     - Open shell in running container"
	@echo "  dev       - Run in development mode"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linter"
	@echo "  compose-up    - Start with Docker Compose"
	@echo "  compose-down  - Stop Docker Compose"
	@echo "  compose-logs  - Show Docker Compose logs"

# Build Docker image
.PHONY: bnp
bnp: build
	@echo "Pushing Docker image $(FULL_IMAGE_NAME) to Docker Hub..."
	docker push $(FULL_IMAGE_NAME)
	@echo "Push completed successfully!"

# Build Docker image
.PHONY: build
build:
	@echo "Building Docker image $(FULL_IMAGE_NAME)..."
	docker build -t $(FULL_IMAGE_NAME) .
	@echo "Build completed successfully!"

# Run container
.PHONY: run
run:
	@echo "Starting container $(CONTAINER_NAME)..."
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):3000 \
		$(FULL_IMAGE_NAME)
	@echo "Container started on http://localhost:$(PORT)"

# Stop container
.PHONY: stop
stop:
	@echo "Stopping container $(CONTAINER_NAME)..."
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	@echo "Container stopped and removed"

# Clean up container and image
.PHONY: clean
clean: stop
	@echo "Removing Docker image $(FULL_IMAGE_NAME)..."
	docker rmi $(FULL_IMAGE_NAME) || true
	@echo "Cleanup completed"

# Show container logs
.PHONY: logs
logs:
	@echo "Showing logs for $(CONTAINER_NAME)..."
	docker logs -f $(CONTAINER_NAME)

# Open shell in running container
.PHONY: shell
shell:
	@echo "Opening shell in $(CONTAINER_NAME)..."
	docker exec -it $(CONTAINER_NAME) /bin/sh

# Development mode (without Docker)
.PHONY: dev
dev:
	@echo "Starting development server..."
	npm run dev

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	npm test

# Run linter
.PHONY: lint
lint:
	@echo "Running linter..."
	npm run lint

# Build and run in one command
.PHONY: build-run
build-run: build run

# Restart container
.PHONY: restart
restart: stop run

# Show container status
.PHONY: status
status:
	@echo "Container status:"
	docker ps -a --filter name=$(CONTAINER_NAME)

# Show image info
.PHONY: info
info:
	@echo "Image information:"
	docker images $(FULL_IMAGE_NAME)

# Docker Compose targets
.PHONY: compose-up
compose-up:
	@echo "Starting services with Docker Compose..."
	docker-compose up -d
	@echo "Services started on http://localhost:$(PORT)"

.PHONY: compose-down
compose-down:
	@echo "Stopping Docker Compose services..."
	docker-compose down
	@echo "Services stopped"

.PHONY: compose-logs
compose-logs:
	@echo "Showing Docker Compose logs..."
	docker-compose logs -f

.PHONY: compose-build
compose-build:
	@echo "Building and starting with Docker Compose..."
	docker-compose up --build -d
	@echo "Services built and started on http://localhost:$(PORT)"
