"""Política de status das reservas."""

from __future__ import annotations

from ..models import ReservationStatus

# Estados válidos entram aqui
BILLABLE_STATUSES = frozenset({ReservationStatus.CONFIRMED})


def is_billable(status: ReservationStatus) -> bool:
    """Indica se a reserva entra nos totais financeiros e de noites."""
    return status in BILLABLE_STATUSES
