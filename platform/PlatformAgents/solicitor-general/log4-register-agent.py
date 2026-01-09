from starlette.responses import JSONResponse
import json
import logging

# Configure logging (Logfire/CloudWatch integration assumed)
logger = logging.getLogger("fasta2a")
logger.setLevel(logging.INFO)

# Example Kafka producer stub (replace with your actual producer)
class KafkaProducerStub:
    def send(self, topic, message):
        logger.info({"topic": topic, "message": message})

kafka_producer = KafkaProducerStub()

class FastA2A(Starlette):
    # ... existing __init__ ...

    def __init__(self, *, storage: Storage, broker: Broker, **kwargs):
        super().__init__(**kwargs)
        self.task_manager = TaskManager(broker=broker, storage=storage)

        # Existing routes
        self.router.add_route(
            '/.well-known/agent-card.json', self._agent_card_endpoint, methods=['HEAD', 'GET', 'OPTIONS']
        )
        self.router.add_route('/', self._agent_run_endpoint, methods=['POST'])

        if self.docs_url is not None:
            self.router.add_route(self.docs_url, self._docs_endpoint, methods=['GET'])

        # NEW: Register route
        self.router.add_route('/register', self._register_agent_endpoint, methods=['POST'])

    async def _register_agent_endpoint(self, request: Request) -> Response:
        """
        Register a visiting agent as a task/event.
        Returns a Registered Agent Card in JSON.
        """
        data = await request.json()

        # Treat registration as a task
        registration_task = {
            "method": "agent/register",
            "params": data,
        }
        task_result = await self.task_manager.create_task(registration_task)

        # Build Registered Agent Card
        registered_card = {
            "name": data.get("name"),
            "url": data.get("url"),
            "version": data.get("version", "1.0.0"),
            "registeredAt": task_result.get("timestamp"),
            "skills": data.get("skills", []),
            "authToken": task_result.get("id"),  # friction-less auth token
        }

        # Emit events to Logfire/CloudWatch/Kafka
        logger.info({"event": "agent_registered", "card": registered_card})
        kafka_producer.send("agent-registrations", registered_card)

        return JSONResponse(content=registered_card)
