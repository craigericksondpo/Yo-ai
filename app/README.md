 /app/README.md
# Logging Model (Contributor Guide)

Recommended .env Template
# Logging backend
LOG_SINK=json          # json | s3 | dynamodb | windows | kafka

# JSON file sink
LOG_PATH=./logs/platform.jsonl

# S3 sink
LOG_S3_BUCKET=my-log-bucket
LOG_S3_PREFIX=platform/logs

# DynamoDB sink
LOG_DDB_TABLE=PlatformLogs

# Windows Event Log sink
WINDOWS_EVENT_SOURCE=YoAIPlatform

# Kafka sink
KAFKA_BROKERS=localhost:9092
KAFKA_TOPIC=yoai-logs


##	Works in: 
-	Lambda
-	Windows
-	Local dev
-	Containers
-	Production

##	Supports: 
-	JSON files
-	S3
-	DynamoDB
-	Windows Event Log
-	Kafka

## Impacts:
-	Switchable via environment variables
-	Zero changes to Logfire
-	Zero changes to your agents
