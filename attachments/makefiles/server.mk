### SERVER
# ¯¯¯¯¯¯¯¯¯¯¯

server.build: ## Build server
	docker-compose build yaml-merger

server.start: ## Start server
	docker-compose up --build yaml-merger

server.services: ## Start main services except the server (for development uses)
	docker-compose up -d main-server-services

server.sh: ## Connect to server to lauch commands
	docker-compose exec yaml-merger sh

server.daemon: ## Start daemon server in its docker container
	docker-compose up --build -d yaml-merger

server.stop: ## Stop server
	docker-compose stop

server.remove: ## Stop server and remove volumes
	docker-compose down -v

server.restart: ## Restart server
	docker-compose down -v && docker-compose up --build -d yaml-merger

server.logs: ## Display server logs
	docker-compose logs -f -t --tail=100