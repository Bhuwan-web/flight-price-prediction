# Variables
COMPOSE_FILE := docker-compose.yml
PROJECT_NAME := flight-price-predictor
MONGO_CONTAINER := mongodb
DB_NAME := flight_price_predictor
MONGO_USER := admin
MONGO_PASSWORD := secret
NGROK_DOMAIN:=model-cockatoo-fair.ngrok-free.app

# Start the backend
.PHONY: run_backend
run_backend:
	@docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d
	@echo "Backend is running."

# Stop the backend
.PHONY: stop_backend
stop_backend:
	@docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down
	@echo "Backend has stopped."

# Load default data into MongoDB
.PHONY: load_default
load_default:
	@echo "Copying dump files to MongoDB container..."
	@docker cp ./dump $(MONGO_CONTAINER):/data/db
	@echo "Restoring data into MongoDB..."
	@docker exec -it $(MONGO_CONTAINER) mongorestore --drop --username $(MONGO_USER) --password $(MONGO_PASSWORD) --authenticationDatabase admin --db=$(DB_NAME) /data/db/dump/$(DB_NAME)
	@echo "Data restored successfully to the database: $(DB_NAME)."

# Drop a specific collection
.PHONY: drop_collection
drop_collection:
	@if [ -z "$(collection)" ]; then \
		echo "Error: Please provide the collection name using 'collection=<collection_name>'."; \
		exit 1; \
	fi
	@docker exec -it $(MONGO_CONTAINER) mongosh --username $(MONGO_USER) --password $(MONGO_PASSWORD) --authenticationDatabase admin --quiet --eval \
		"db = db.getSiblingDB('$(DB_NAME)'); if (db.getCollection('$(collection)').exists()) { db.$(collection).drop(); print('Collection $(collection) dropped successfully.'); } else { print('Collection $(collection) does not exist.'); }"

# Drop all collections
.PHONY: drop_all
drop_all:
	@docker exec -it $(MONGO_CONTAINER) mongosh --username $(MONGO_USER) --password $(MONGO_PASSWORD) --authenticationDatabase admin --quiet --eval \
		"db = db.getSiblingDB('$(DB_NAME)'); for (coll in db.getCollectionNames()) { db.getCollection(coll).drop(); print('Collection ' + coll + ' dropped successfully.'); }"
.PHONY: host
host:
	@echo "Hosting local service on "
	@ngrok http --domain=$(NGROK_DOMAIN) 0.0.0.0:8000

.PHONY: run_and_host
run_and_host:
	@make run_backend
	@make host

.PHONY: mongo_shell
mongo_shell:
	@docker exec -it $(MONGO_CONTAINER) mongosh --username $(MONGO_USER) --password=$(MONGO_PASSWORD) --authenticationDatabase admin
