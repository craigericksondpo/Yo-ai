# core/platform_agent.py

from __future__ import annotations
from core.yoai_agent import YoAiAgent
from typing import Dict, List, Callable, Any


# ---------------------------------------------------------------------------
# PlatformEventBus
# ---------------------------------------------------------------------------

class PlatformEventBus:
    """
    In-process async pub/sub event bus for PlatformAgents.

    Lifecycle:
      - Instantiated once at platform startup.
      - Injected into every PlatformAgent at construction.
      - Each PlatformAgent auto-registers its handler on init.

    Usage:
      - Agents subscribe via subscribe(event_type, handler).
      - Agents broadcast via broadcast(event_type, event).
      - Only live, constructed instances are in the registry.

    Thread safety:
      - Designed for single-process asyncio use.
      - Not safe for concurrent modification from multiple threads.

    Note:
      The PlatformEventBus handles intra-process coordination between
      PlatformAgents (CM-6 config changes, lifecycle events).
      Cross-agent platform events are published to Kafka via the
      Kafka Observability Publisher (a separate component, not yet built).
      These are two distinct layers — the event bus is NOT a log sink.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """
        Register a handler for a given event type.
        Called automatically by PlatformAgent.__init__().
        """
        self._subscribers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """
        Remove a handler for a given event type.
        Call during agent teardown to avoid stale references.
        """
        handlers = self._subscribers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)

    async def broadcast(self, event_type: str, event: dict) -> None:
        """
        Fan out event to all handlers subscribed to event_type.
        Handlers are awaited sequentially. Exceptions are not suppressed —
        callers should wrap broadcast() in a try/except if isolation is needed.
        """
        for handler in list(self._subscribers.get(event_type, [])):
            await handler(event)

    @property
    def subscriber_count(self) -> Dict[str, int]:
        """
        Diagnostic: returns a count of registered handlers per event type.
        """
        return {k: len(v) for k, v in self._subscribers.items()}


# ---------------------------------------------------------------------------
# PlatformAgent
# ---------------------------------------------------------------------------

class PlatformAgent(YoAiAgent):
    """
    PlatformAgent:
    Privileged, long-lived, platform-service agent.

    Responsibilities:
      - Inherit all loading behavior from YoAiAgent (skills, tools, schemas,
        fingerprints, knowledge)
      - Enforce platform-level constraints (call graph, trust tiers, etc.)
      - Expose platform services to YoAiAgents and Visiting Agents
      - Maintain singleton-like lifecycle (managed by the platform)
      - Receive and optionally react to platform configuration changes (CM-6)
      - Emit configuration change events when modifying platform behavior

    PlatformAgents do NOT use profiles — they do not represent people.
    PlatformAgents act on behalf of the Platform as brokers and services.

    Card Contract:
      PlatformAgents expose the basic card only — the extended card is
      NEVER exposed externally, even to registered callers. Some PlatformAgents
      may not have an extended card at all — this is always valid under A2A spec.

    Event Bus:
      - A PlatformEventBus must be injected at construction.
      - This agent auto-registers its on_platform_configuration_change handler
        for the "Platform.ConfigurationChanged" event on init.
      - On teardown, call shutdown() to unsubscribe and release references.
    """

    PLATFORM_CONFIG_EVENT = "Platform.ConfigurationChanged"

    def __init__(
        self,
        *,
        card: dict | None = None,
        extended_card: dict | None = None,
        context=None,
        event_bus: PlatformEventBus,
    ):
        super().__init__(
            card=card,
            extended_card=extended_card,
            profile=None,       # PlatformAgents never use profiles
            context=context,
        )

        if not isinstance(event_bus, PlatformEventBus):
            raise TypeError(
                f"PlatformAgent '{self.actor_name}' requires a PlatformEventBus instance. "
                f"Got: {type(event_bus).__name__}"
            )

        self.event_bus = event_bus

        # Auto-register this instance for configuration change events
        self.event_bus.subscribe(
            self.PLATFORM_CONFIG_EVENT,
            self.on_platform_configuration_change,
        )

        self.log(
            event_type="platform_agent_registered",
            message=f"{self.actor_name} registered on PlatformEventBus",
            payload={"event_type": self.PLATFORM_CONFIG_EVENT},
        )

    # ------------------------------------------------------------------
    # showCard() — basic card only, always
    # ------------------------------------------------------------------
    def showCard(self, context=None) -> dict:
        """
        Return the basic card only.

        PlatformAgent behavior:
          - No card: fires NO_CARD alert event (three bells), returns {}.
          - Any caller, any context: always returns the basic card only.
            PlatformAgents never expose their extended card externally.
            Some PlatformAgents may have no extended card — always valid.

        The basic card is the public A2A advertised contract. It describes
        what the PlatformAgent can do and how to reach it. The extended
        card contains internal platform configuration and is not for
        external consumption.

        Args:
            context: AgentContext from the current request, if available.
                     Not used for access decisions — included for API
                     consistency with BaseAgent and YoAiAgent.

        Returns:
            dict: basic card, or {} if no card is available.
        """
        if not self.card:
            self._fire_no_card_event(context)
            return {}

        return self.card

    # ------------------------------------------------------------------
    # CM-6: Receive configuration change notifications
    # ------------------------------------------------------------------
    async def on_platform_configuration_change(self, event: dict) -> None:
        """
        Called when any PlatformAgent broadcasts a ConfigurationChanged event.
        PlatformAgents may override this to react — base implementation logs only.

        NIST 800-53 CM-6: Configuration Settings.
        """
        self.log(
            event_type="platform_config_change_received",
            message=f"[CM-6] Configuration change received: {event.get('type')}",
            payload=event,
        )

    # ------------------------------------------------------------------
    # CM-6: Emit configuration change events
    # ------------------------------------------------------------------
    async def emit_configuration_changed(
        self,
        change_type: str,
        details: dict | None = None,
    ) -> None:
        """
        Broadcast a Platform.ConfigurationChanged event to all subscribed
        PlatformAgents via the injected PlatformEventBus.

        This publishes to the in-process PlatformEventBus only.
        Cross-agent Kafka publishing is handled by the Kafka Observability
        Publisher (a separate component, not yet built).

        NIST 800-53 CM-6: Configuration Settings.
        """
        event = {
            "type": change_type,
            "details": details or {},
            "source": self.actor_name,
        }

        self.log(
            event_type="platform_config_change_emitted",
            message=f"[CM-6] Broadcasting configuration change: {change_type}",
            payload=event,
        )

        await self.event_bus.broadcast(self.PLATFORM_CONFIG_EVENT, event)

    # ------------------------------------------------------------------
    # Teardown: unsubscribe from event bus
    # ------------------------------------------------------------------
    def shutdown(self) -> None:
        """
        Unsubscribe this agent from the event bus.
        Call during platform teardown or agent lifecycle end
        to prevent stale handler references.
        """
        self.event_bus.unsubscribe(
            self.PLATFORM_CONFIG_EVENT,
            self.on_platform_configuration_change,
        )

        self.log(
            event_type="platform_agent_unregistered",
            message=f"{self.actor_name} unsubscribed from PlatformEventBus",
            payload={"event_type": self.PLATFORM_CONFIG_EVENT},
        )
