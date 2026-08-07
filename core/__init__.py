"""MURMUROS core: delt infrastruktur for agent-samarbeid.

Eksponerer hendelsesmodellen (`Event`) og pub/sub-tavlen (`MurmurBlackboard`)
som agentene kommuniserer gjennom.
"""

from core.blackboard import Event, MurmurBlackboard

__all__ = ['Event', 'MurmurBlackboard']
