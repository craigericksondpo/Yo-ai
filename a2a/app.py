# yo_ai_main/a2a/app.py - FastA2AApp instance

from fasta2a import FastA2AApp

# This is the shared FastA2A runtime instance used across the platform.
# Starlette will mount this under /a2a/* in app/main.py.
a2a_app = FastA2AApp()
