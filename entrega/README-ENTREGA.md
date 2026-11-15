# Entrega do Desafio — Consolidador de Reservas de Hotel

## 1. Defeitos Corrigidos e Causas Raízes

1. **Inclusão indevida de status não faturáveis nos totais**
   * **Causa raiz:** O método is_billable verificava apenas se o status era diferente de CANCELLED, permitindo que reservas com status NO_SHOW e quaisquer outros status que fossem adicionados posteriomente entrassem indevidamente nos totais faturáveis e de noites.

2. **Cálculo incorreto das noites de estadia**
   * **Causa raiz:** O cálculo subtraía apenas o dia do mês (checkout.day - checkin.day), gerando resultados incorretos ou negativos em estadias que cruzavam a virada de mês ou ano.

3. **Inversão da operação e imprecisão na conversão cambial**
   * **Causa raiz:** A função de conversão dividia o valor pela taxa cambial em vez de multiplicar e realizava conversões intermediárias para float, introduzindo perda de precisão decimal.

4. **Ordenação invertida no ranking dos melhores hotéis (top_hotels)**
   * **Causa raiz:** A chave de ordenação utilizava o montante em ordem crescente (menor valor primeiro) em vez de decrescente, além de não prever o desempate por hotel_id ascendente.

5. **Interrupção na leitura do arquivo CSV**
   * **Causa raiz:** O repositório continha uma limitação que interrompia o processamento ao atingir 200 linhas, descartando todas as reservas após esse limite no arquivo de entrada.

6. **Ausência de validação e tipagem formal dos estados de reserva**
   * **Causa raiz:** O modelo e o parser tratavam o status como strings genéricas sem validação de domínio, o que permitia a passagem de status desconhecidos ou inválidos sem apontar erro. Corrigi introduzindo a enumeração ReservationStatus (StrEnum) na estrutura da entidade Reservation e no parser do CSV.

---

## 2. Como o Problema Foi Investigado e Abordado

1. **Execução inicial e análise de falhas dos testes:**
   * Executei os testes inicialmente para mapear em que arquivo os erros estavam e de quais funções se tratavam.

2. **Depuração linha a linha com VS Code Debugger:**
   * Inspecionei o fluxo de execução utilizando o debugger do VS Code, mantendo a configuração salva em [.vscode/launch.json](../.vscode/launch.json) para facilitar a reprodução do ambiente. A partir do mapeamento inicial, adicionei breakpoints nas funções que apresentavam erro para analisar as variáveis e o fluxo dos dados em tempo de execução. Tenho mais costume de realizar depurações de forma manual utilizando o GDB (em C/C++), porém a dinâmica se mostrou extremamente semelhante. Considero que acompanhar a execução linha a linha, vendo como cada linha se comporta aproxima muito mais do código e faz com que suas ideias se concretizem melhor na mente, excepcionalmente por se tratar de um código 'pronto' que não participei da implementação.

3. **Inspeção de código e regras de negócio:**
   * Comparei as implementações existentes com as especificações do README principal (fórmula de cálculo de noites, uso de Decimal e arredondamento HALF_UP, política restrita de faturamento para CONFIRMED e regras de ordenação de ranking e meses), deixando o comportamento conforme o especificado nas regras de negócio.

4. **Correções pontuais e arquitetura modular:**
   * As mudanças foram pensadas para serem totalmente modulares, orientadas pela ideia de que cada commit descreva exatamente o que faz, mantendo coesão estrita e sem criar dependências entre partes diferentes do sistema. Corrigi cada defeito em seu respectivo módulo (status_policy, stay_calculator, currency_converter, report_builder e csv_reservation_repository).

5. **Refatoração estrutural com Enum:**
   * Criei a enumeração ReservationStatus para reforçar a consistência tipada da entidade Reservation, integrando sua validação no RowParser e centralizando os estados faturáveis.

6. **Criação de suíte de testes de casos de borda:**
   * Para não modificar os testes originais fornecidos, criei arquivos dedicados com sufixo extra cobrindo cenários complexos (virada de ano, anos bissextos, estadias de zero noites, desempate no ranking, moedas inexistentes e agrupamento mensal), buscando garantir o comportamento esperado nos casos mais extremos.

---

## 3. Como Validar

Validei o projeto em múltiplas frentes para garantir a exatidão e a integridade de ponta a ponta:

1. **Bateria de testes automatizados:**
   * Executei todos os testes fornecidos no projeto original em conjunto com os novos testes que criei, assegurando que as regras de negócio e os casos de borda se mantêm íntegros

2. **Validação contra a amostra oficial:**
   * Rodei o CLI com a base de validação e comparei o JSON de saída com os valores tabelados no README (totais, agregações por mês e melhores hotéis):
   ```bash
   PYTHONPATH=src python -m onfly_report \
     --input data/exemplo-validacao.csv \
     --rates data/taxas_cambio.csv \
     --output output/exemplo.json
   ```

3. **Validação na base completa de reservas:**
   * Executei o CLI sobre a base completa para inspecionar os totais consolidados, a consistência dos agrupamentos mensais e a ausência de travamentos ou divisões por zero:
   ```bash
   PYTHONPATH=src python -m onfly_report \
     --input data/reservas_hoteis.csv \
     --rates data/taxas_cambio.csv \
     --output output/report.json
   ```

> **Nota sobre consistência das entradas:**  
> Como o README garante explicitamente que os dados fornecidos estão consistentes e os defeitos estão no CLI, optei por não implementar verificações defensivas adicionais de integridade dos arquivos (como tratamento de linhas corrompidas ou campos faltantes fora do fluxo padrão). Caso o contrato de negócio não garantisse essa consistência prévia, eu me atentaria a este detalhe e incluiria camadas extras de validação e tolerância a falhas na ingestão dos dados.

---

## 4. Resultado dos Testes (pytest)

Execução do comando:
```bash
pytest -v
```

Saída obtida (todos os testes fornecidos e os novos testes adicionais passam com sucesso):
```text
============================= test session starts ==============================
platform darwin -- Python 3.11.x, pytest-8.x.x
collected 30 items

tests/test_by_month_extra.py ....                                        [ 13%]
tests/test_currency.py .                                                 [ 16%]
tests/test_currency_extra.py .....                                       [ 33%]
tests/test_nights.py .                                                   [ 36%]
tests/test_nights_extra.py ......                                        [ 56%]
tests/test_regression_report.py .                                        [ 60%]
tests/test_status_rules.py .                                             [ 63%]
tests/test_status_extra.py ......                                        [ 83%]
tests/test_top_hotels.py .                                               [ 86%]
tests/test_top_hotels_extra.py ....                                      [100%]

============================== 30 passed in 0.45s ==============================
```
