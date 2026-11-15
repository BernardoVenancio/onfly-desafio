"""Testes adicionais e casos de borda: câmbio, precisão decimal e arredondamento."""

from decimal import Decimal
import pytest
from helpers import run_cli
from onfly_report.services.currency_converter import convert_to_brl
from onfly_report.services.report_builder import format_money


def test_convert_to_brl_preserves_decimal_exactness():
    """A conversão deve manter precisão Decimal sem conversão intermediária para float."""
    rates = {"USD": Decimal("5.420000"), "EUR": Decimal("5.880000"), "BRL": Decimal("1.000000")}
    result = convert_to_brl(Decimal("100.50"), "USD", rates)
    assert isinstance(result, Decimal)
    assert result == Decimal("544.710000")


def test_convert_to_brl_with_unknown_currency_raises_key_error():
    """Tentar converter uma moeda não cadastrada na tabela de taxas deve levantar KeyError."""
    rates = {"USD": Decimal("5.420000"), "BRL": Decimal("1.000000")}
    with pytest.raises(KeyError):
        convert_to_brl(Decimal("100.00"), "GBP", rates)


def test_format_money_rounds_half_up():
    """O arredondamento monetário deve seguir a regra HALF_UP estritamente."""
    # 0.005 arredonda para cima (0.01) no HALF_UP
    assert format_money(Decimal("100.005")) == "100.01"
    # 0.004 arredonda para baixo (0.00)
    assert format_money(Decimal("100.004")) == "100.00"
    # 0.0050 em número par (float round arredondaria para 0.00, HALF_UP deve ir para 0.01)
    assert format_money(Decimal("0.005")) == "0.01"
    assert format_money(Decimal("0.015")) == "0.02"


def test_currency_conversion_eur(tmp_path):
    """Conversão de EUR para BRL usando a taxa informada."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "currency": "EUR", "amount": "150.00"},
        ],
    )
    # 150.00 * 5.88 = 882.00
    assert report["summary"]["total_amount_brl"] == "882.00"


def test_mixed_currencies_total_amount(tmp_path):
    """Soma de múltiplas moedas no mesmo relatório deve ser exata."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "currency": "BRL", "amount": "100.00"},
            {"reservation_id": "R-2", "currency": "USD", "amount": "200.00"},  # 200 * 5.42 = 1084.00
            {"reservation_id": "R-3", "currency": "EUR", "amount": "50.00"},   # 50 * 5.88 = 294.00
        ],
    )
    # 100.00 + 1084.00 + 294.00 = 1478.00
    assert report["summary"]["total_amount_brl"] == "1478.00"
