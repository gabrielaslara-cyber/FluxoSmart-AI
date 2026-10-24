# FluxoSmart AI 📊

Dashboard de análise de vendas para pequenos negócios, desenvolvido por **Gabriela de Souza Lara** em **Python e Streamlit**.

> **MVP demonstrativo:** a versão atual oferece análise descritiva de dados, sem IA generativa. Funcionalidades de IA estão no planejamento futuro.

## Funcionalidades

- Upload de arquivos Excel (`.xlsx`) ou CSV;
- Indicadores de faturamento, quantidade vendida e ticket médio;
- Filtros por categoria e período;
- Gráficos de faturamento diário e por categoria;
- Exportação dos dados filtrados para CSV;
- Exemplo de vendas fictícias em `data/vendas_exemplo.csv`;
- Testes automatizados com pytest.

## Instalação

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Como usar

1. Execute `streamlit run app.py`.
2. Explore os dados fictícios carregados automaticamente ou envie sua planilha Excel/CSV.
3. Filtre categorias e datas, analise os gráficos e exporte os dados.

### Formato esperado

| Coluna | Tipo | Exemplo |
|---|---|---|
| `data` | data | `2026-01-15` |
| `produto` | texto | `Café` |
| `categoria` | texto | `Alimentos` |
| `quantidade` | positivo | `2` |
| `preco_unitario` | número não negativo (R$) | `12.50` |
| `pedido_id` | texto, opcional | `P001` |

Com `pedido_id`, o ticket médio considera pedidos distintos; sem ele, considera registros. Não são contabilizados descontos, impostos e devoluções.

## Testes

```bash
python -m pytest -q
```

## Estrutura

```text
app.py
fluxosmart/
  __init__.py
  analytics.py
data/
  vendas_exemplo.csv
tests/
  test_analytics.py
.streamlit/
  config.toml
requirements.txt
README.md
```

## Próximas etapas

- Indicadores de margem, custos e metas;
- Comparativos mensais;
- Alertas de tendências com metodologia explicável;
- Assistente de IA com fontes, limites e supervisão humana;
- Publicação de uma demonstração em nuvem.

## Privacidade

Os dados de demonstração são fictícios. Não publique dados pessoais ou comerciais sigilosos no repositório público.

## Autoria e licença

**Gabriela de Souza Lara** — portfólio de programação Python, análise de dados e aplicações web.

Distribuído sob a [Licença MIT](LICENSE).
