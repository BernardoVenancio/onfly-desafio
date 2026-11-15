"""Testes adicionais e casos de borda: regras de status e tipos."""

import pytest
from helpers import run_cli
from onfly_report.exceptions import InputFileError
from onfly_report.models import RawRow, ReservationStatus
from onfly_report.services.row_parser import RowParser
from onfly_report.services.status_policy import is_billable


def test_reservation_status_matches_string_values():
    """Os valores da enum correspondem às strings do CSV."""
    assert ReservationStatus("CONFIRMED") is ReservationStatus.CONFIRMED
    assert ReservationStatus("CANCELLED") is ReservationStatus.CANCELLED
    assert ReservationStatus("NO_SHOW") is ReservationStatus.NO_SHOW
    assert ReservationStatus.NO_SHOW == "NO_SHOW"


def test_only_confirmed_is_billable():
    """Apenas confirmed é faturável."""
    assert is_billable(ReservationStatus.CONFIRMED)
    assert not is_billable(ReservationStatus.CANCELLED)
    assert not is_billable(ReservationStatus.NO_SHOW)


def test_invalid_status_raises_value_error():
    """Status que não pertence a ReservationStatus deve levantar ValueError."""
    with pytest.raises(ValueError):
        ReservationStatus("INVALID_STATUS")

    with pytest.raises(ValueError):
        ReservationStatus("PENDING")

    with pytest.raises(ValueError):
        ReservationStatus("")


def test_row_parser_with_unknown_status_raises_input_file_error():
    """Linha com status desconhecido no CSV deve resultar em InputFileError."""
    parser = RowParser()
    raw = RawRow(
        line_number=2,
        values={
            "reservation_id": "R-1",
            "checkin_date": "2025-01-10",
            "checkout_date": "2025-01-12",
            "rooms": "1",
            "status": "UNKNOWN_STATUS",
            "currency": "BRL",
            "amount": "100.00",
        },
    )
    with pytest.raises(InputFileError, match="linha 2 inválida"):
        parser.parse(raw)


def test_row_parser_strips_whitespace_around_status():
    """Espaços em branco antes ou depois do status devem ser removidos."""
    parser = RowParser()
    raw = RawRow(
        line_number=2,
        values={
            "reservation_id": "R-1",
            "checkin_date": "2025-01-10",
            "checkout_date": "2025-01-12",
            "rooms": "1",
            "status": "  CONFIRMED  ",
            "currency": "BRL",
            "amount": "100.00",
        },
    )
    reservation = parser.parse(raw)
    assert reservation.status is ReservationStatus.CONFIRMED


def test_returns_zero_totals_without_confirmed_reservations(tmp_path):
    """Se todos cancelarem, o retorno financeiro e de noites é zero."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CANCELLED", "amount": "50.00"},
            {"reservation_id": "R-2", "status": "NO_SHOW", "amount": "20.00"},
        ],
    )
    summary = report["summary"]
    assert summary["total_reservations"] == 2
    assert summary["total_amount_brl"] == "0.00"
    assert summary["total_room_nights"] == 0
    assert summary["average_nightly_rate_brl"] == "0.00"
    assert report["by_month"] == []
    assert report["top_hotels"] == []
