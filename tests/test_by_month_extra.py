"""Testes adicionais e casos de borda: agregação por mês (by_month)."""

from helpers import run_cli


def test_by_month_attributes_all_nights_and_amount_to_checkin_month(tmp_path):
    """Estadia que cruza a virada de mês deve ser atribuída integralmente ao mês de check-in."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-01-30",
                "checkout_date": "2025-02-02",
                "rooms": "1",
                "amount": "300.00",
                "currency": "BRL",
                "status": "CONFIRMED",
            }
        ],
    )
    # Deve conter apenas janeiro, sem criar entrada para fevereiro
    assert len(report["by_month"]) == 1
    assert report["by_month"][0] == {
        "month": "2025-01",
        "reservations": 1,
        "room_nights": 3,
        "total_brl": "300.00",
    }


def test_by_month_sorted_chronologically(tmp_path):
    """O array by_month deve ser retornado ordenado de forma ascendente pelo mês."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "checkin_date": "2025-05-10", "checkout_date": "2025-05-12", "amount": "100.00"},
            {"reservation_id": "R-2", "checkin_date": "2024-12-20", "checkout_date": "2024-12-22", "amount": "100.00"},
            {"reservation_id": "R-3", "checkin_date": "2025-01-15", "checkout_date": "2025-01-16", "amount": "100.00"},
            {"reservation_id": "R-4", "checkin_date": "2025-03-01", "checkout_date": "2025-03-03", "amount": "100.00"},
        ],
    )
    months = [item["month"] for item in report["by_month"]]
    assert months == ["2024-12", "2025-01", "2025-03", "2025-05"]


def test_by_month_aggregates_multiple_reservations(tmp_path):
    """Múltiplas reservas no mesmo mês devem ser somadas corretamente."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-04-01",
                "checkout_date": "2025-04-04",
                "rooms": "1",
                "amount": "300.00",
            },
            {
                "reservation_id": "R-2",
                "checkin_date": "2025-04-10",
                "checkout_date": "2025-04-12",
                "rooms": "2",
                "amount": "400.00",
            },
        ],
    )
    assert len(report["by_month"]) == 1
    assert report["by_month"][0] == {
        "month": "2025-04",
        "reservations": 2,
        "room_nights": 7,  # 3 noites (1 quarto) + 2 noites * 2 quartos = 7
        "total_brl": "700.00",
    }


def test_by_month_excludes_cancelled_and_no_show(tmp_path):
    """Reservas canceladas ou no-show não devem aparecer no by_month."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "checkin_date": "2025-06-01", "checkout_date": "2025-06-03", "status": "CANCELLED"},
            {"reservation_id": "R-2", "checkin_date": "2025-07-01", "checkout_date": "2025-07-03", "status": "NO_SHOW"},
            {"reservation_id": "R-3", "checkin_date": "2025-08-01", "checkout_date": "2025-08-03", "status": "CONFIRMED", "amount": "200.00"},
        ],
    )
    months = [item["month"] for item in report["by_month"]]
    assert months == ["2025-08"]
