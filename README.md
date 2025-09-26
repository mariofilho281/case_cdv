# Dados de Aerogeradores no Brasil

Nesse projeto, foram desenvolvidas rotinas para coleta, tratamento, e armazenamento de dados de aerogeradores do ArcGIS do SIGEL/ANEEL. Esses dados são posteriormente utilizados em um [*dashboard*](https://public.tableau.com/views/CaseCdV/Painel1?:language=pt-BR&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) com visualizações interessantes sobre o setor de energia eólica no Brasil.

## Arquivos do projeto

- `notebooks/`:
  - `data_cleanup.ipynb`: principal arquivo, que pode ser executado para reproduzir os passos de coleta, tratamento, e armazenamento dos dados.
- `outputs/`:
  - `output.csv`: todos os dados tratados pelo *notebook* acima.
  - `data_for_dashboard.csv`: dados com apenas as colunas utilizadas no *dashboard*. 
- `scripts/`:
  - `fetch_data.py`: contém a classe `DataFetcher`, que faz a coleta dos dados da Internet.
  - `power_model.py`: ajusta um [modelo quadrático](https://kirkwood.pressbooks.pub/windenergy/chapter/theoretical-power-of-wind/) entre potência e diâmetro do rotor dos aerogeradores.
- `tests/`:
  - `test_fetch_data.py`: alguns testes para a classe `DataFetcher`. 

## *Disclaimer*

Esse projeto foi feito no âmbito de processo seletivo para a área de *Data Analytics* da empresa Casa dos Ventos, com o objetivo de avaliar as habilidades do candidato em análise de dados.

No *dashboard*, eu incluí visualizações que mostram padrões interessantes identificados na análise exploratória dos dados. Todavia, meu conhecimento do setor de energia eólica é superficial, então algum detalhe pode ter me escapado durante a análise,

Mesmo sem a intuição de um especialista (que faz toda diferença na tarefa de análise de dados), acredito que pude demonstrar minhas habilidades nos quesitos avaliados.
