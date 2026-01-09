 # Build Registered Agent Card
        registered_card = {
            "name": data.get("name"),
            "url": data.get("url"),
            "version": data.get("version", "1.0.0"),
            "registeredAt": task_result.get("timestamp"),
            "skills": data.get("skills", []),
            "authToken": task_result.get("id"),  # friction-less auth token
        }
