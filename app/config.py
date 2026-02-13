# yo_ai_main/app/config.py - env vars, settings, logfire config

import logfire
import os

def configure_logging():
    environment = os.getenv("YOAI_ENV", "local")

    logfire.configure(
        service_name="yoai-platform",
        level="INFO",
        json_output=True,
        include={
            "environment": environment,
            "service": "yoai-platform",
        },
        redact=[
            "password",
            "secret",
            "token",
            "apiKey",
        ],
    )

    # Optional: add a Kafka sink later
    # logfire.add_sink(KafkaSink(...))

    return logfire
