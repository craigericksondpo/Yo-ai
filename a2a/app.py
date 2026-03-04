# yo_ai_main/a2a/app.py - FastA2AApp instance
# THIS IS AN OPTION FOR FastA2A and STARLETTE and Google ADK

from fasta2a import FastA2AApp

# This is NOT a shared runtime instance used across the Yo-ai platform.
# Starlette will mount this under /a2a/* in app/main.py.
a2a_app = FastA2AApp()

