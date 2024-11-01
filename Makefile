.DEFAULT_GOAL := help


docker_test_up:
	sudo docker compose -f docker-compose.test.yml up -d

docker_test_down:
	sudo docker compose -f docker-compose.test.yml down

docker_up:
	sudo docker compose -f docker-compose.dev.yml up --build -d

docker_down:
	sudo docker compose -f docker-compose.dev.yml down

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands: "
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
