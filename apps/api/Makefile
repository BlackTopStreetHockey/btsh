.PHONY: help
help: ## Show this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: build up clean
build: ## Build all images.
	docker compose build --pull --parallel
up: ## Start containers, defaulting to all if S= is not specified. Usage: make up S="api postgres".
	docker compose up --attach-dependencies $(S)
clean: ## Kill and force remove containers.
	docker compose kill
	docker compose rm -f

.PHONY: bash bash-cmd
bash: ## Start a bash shell inside a new docker container. Usage make bash S=api.
	docker compose run --rm $(S) bash
bash-cmd: ## Run a bash command inside a new docker container. Usage: make bash-cmd S=api C="python".
	docker compose run --rm $(S) bash -c "$(C)"

.PHONY: manage makemigrations migrate shell
manage: ## Run a django management command. Usage: make manage C="makemigrations".
	docker compose run --rm api bash -c "python manage.py $(C)"
makemigrations: ## Create new django migrations.
	@$(MAKE) manage C=makemigrations
migrate: ## Apply django migrations.
	@$(MAKE) manage C=migrate
shell: ## Start a django shell with models and common django utils already imported.
	@$(MAKE) manage C=shell_plus

.PHONY: sync
sync: clean build migrate ## Sync the project.
