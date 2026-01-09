async def register_agent(request: Request) -> Response:
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
        "version": "1.0.0",
        "registeredAt": task_result["timestamp"],
        "skills": data.get("skills", []),
        "authToken": task_result["id"],  # could be used for friction-less auth
    }

    # Log to CloudWatch / Kafka
    logger.info({"event": "agent_registered", "card": registered_card})
    kafka_producer.send("agent-registrations", registered_card)

    return Response(content=json.dumps(registered_card), media_type="application/json")
