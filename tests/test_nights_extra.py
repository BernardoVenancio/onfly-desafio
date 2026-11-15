"""Testes adicionais e casos de borda: cálculo de noites."""

from helpers import run_cli


def test_nights_across_year_boundary(tmp_path):
    """A diferença entre as datas considera corretamente a virada de ano."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-12-31",
                "checkout_date": "2026-01-01",
                "rooms": "1",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 1


def test_multiple_rooms(tmp_path):
    """O cálculo das noites deve levar em consideração o número de quartos reservados."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-08-06",
                "checkout_date": "2025-08-11",
                "rooms": "5",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 25


def test_single_night_reservation(tmp_path):
    """Uma hospedagem de uma noite deve contabilizar uma noite no quarto."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-08-06",
                "checkout_date": "2025-08-07",
                "rooms": "1",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 1


def test_same_day_checkin_and_checkout(tmp_path):
    """Check-in e check-out no mesmo dia resultam em zero noites e diária média 0.00."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-08-06",
                "checkout_date": "2025-08-06",
                "rooms": "1",
                "amount": "150.00",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 0
    assert report["summary"]["average_nightly_rate_brl"] == "0.00"


def test_nights_across_non_leap_year_february(tmp_path):
    """O cálculo considera corretamente fevereiro em anos não bissextos."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-02-27",
                "checkout_date": "2025-03-02",
                "rooms": "1",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 3


def test_nights_across_leap_year_february(tmp_path):
    """O cálculo considera corretamente o dia adicional de fevereiro em anos bissextos."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2024-02-27",
                "checkout_date": "2024-03-02",
                "rooms": "1",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 4
