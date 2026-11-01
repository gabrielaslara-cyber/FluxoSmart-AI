# FluxoSmart AI Premium — Portfólio de Python e Business Intelligence

**Aplicação web demonstrativa** para transformar planilhas de vendas em indicadores, gráficos, diagnósticos descritivos e relatórios gerenciais em PDF. Criada por **Gabriela de Souza Lara** com Python, Streamlit, Pandas e ReportLab.

**[Experimentar o aplicativo online](https://fluxosmart-ai-premium.streamlit.app/)** · [Código desta versão](https://github.com/gabrielaslara-cyber/FluxoSmart-AI/tree/feature/relatorio-premium)

> **Transparência:** análises baseadas em regras, sem IA generativa ou previsões. Resultados demonstrados com dados fictícios. Não substitui avaliação de custos, margem e estoque.

## Funcionalidades da versão Premium

- Importação de dados Excel/CSV e filtros por categoria e período.
- Faturamento, unidades vendidas, pedidos e ticket médio.
- Gráficos por categoria, produto e evolução das vendas.
- Diagnósticos por regras: categoria líder, produto mais vendido e comparação entre dias com vendas.
- Download de dados filtrados em CSV e **relatório gerencial PDF de duas páginas**, incluindo gráficos, diagnósticos, recomendações e data de emissão.

## Demonstração validada

Com a planilha fictícia de 01/01 a 08/01/2026, o relatório gerado apresentou **R$ 311,50** de faturamento, **34 unidades**, **8 pedidos**, **R$ 38,94** de ticket médio, categoria líder **Papelaria (54,7%)**, produto mais vendido em unidades **Caneta (17)** e variação de **−22,0%** na comparação descritiva entre metades dos dias com vendas.

**Estado:** geração de PDF e indicadores validados com dados de exemplo. Testes abrangentes com planilhas externas, múltiplos formatos e casos extremos ainda são necessários antes de uso comercial.

## Executar a versão premium localmente

```bash
pip install -r requirements.txt
streamlit run app_premium.py
```

**Tecnologias:** Python · Streamlit · Pandas · ReportLab · GitHub · pytest

## Formato da planilha

| Coluna | Tipo |
|---|---|
| `data` | data |
| `produto` | texto |
| `categoria` | texto |
| `quantidade` | número positivo |
| `preco_unitario` | preço não negativo |
| `pedido_id` | opcional |

## Próximos passos

Validar casos extremos e planilhas adicionais, melhorar testes de interface, criar capturas de tela do dashboard e expandir diagnósticos com custos e margens. IA generativa é uma possibilidade futura, não recurso disponível.

## Autoria

**Gabriela de Souza Lara** · [Perfil GitHub](https://github.com/gabrielaslara-cyber)

---
