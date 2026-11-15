"""Testes adicionais e casos de borda: ranking de hotéis."""

from helpers import run_cli


def test_sorts_by_amount_then_hotel_id(tmp_path):
    """O ranking ordena por valor decrescente e desempata por hotel_id crescente."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H04", "hotel_name": "Hotel D", "amount": "1000.00"},
            {"reservation_id": "R-2", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "900.00"},
            {"reservation_id": "R-3", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "900.00"},
            {"reservation_id": "R-4", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "1100.00"},
        ],
        top=3,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H02", "H04", "H01"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["1100.00", "1000.00", "900.00"]


def test_top_exceeds_available_hotels(tmp_path):
    """O ranking deve ficar limitado aos hotéis disponíveis mesmo que o top seja um valor superior."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "1000.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "900.00"},
            {"reservation_id": "R-3", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "1200.00"},
        ],
        top=5,
    )
    assert len(report["top_hotels"]) == 3
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H03", "H02", "H01"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["1200.00", "1000.00", "900.00"]


def test_handles_single_hotel(tmp_path):
    """O comportamento deve se manter o mesmo quando apenas um hotel estiver disponível"""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "1000.00"},
        ],
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["1000.00"]


def test_breaks_ties_by_hotel_id(tmp_path):
    """O ranking deve ordenar por ID do hotel caso o valor de todos forem iguais."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H04", "hotel_name": "Hotel D", "amount": "1000.00"},
            {"reservation_id": "R-2", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "1000.00"},
            {"reservation_id": "R-3", "hotel_id": "H05", "hotel_name": "Hotel E", "amount": "1000.00"},
            {"reservation_id": "R-4", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "1000.00"},
            {"reservation_id": "R-5", "hotel_id": "H07", "hotel_name": "Hotel F", "amount": "1000.00"},
            {"reservation_id": "R-6", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "1000.00"},
            {"reservation_id": "R-7", "hotel_id": "H06", "hotel_name": "Hotel G", "amount": "1000.00"},
        ],
        top=4,
    )
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H01", "H02", "H03", "H04"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["1000.00", "1000.00", "1000.00", "1000.00"]
