# Análise Topológica e Algorítmica da Rede Wikispeedia

Este repositório contém o código-fonte para a análise estrutural, avaliação algorítmica e exploração de propriedades de redes complexas sobre o grafo de navegação **Wikispeedia** (fornecido pelo *Stanford Network Analysis Project - SNAP*). 

## Estrutura do Projeto

O repositório está organizado da seguinte forma

```text
                     
├── part2/                          # Implementação dos algoritmos da parte 2
│   ├── bellman_ford.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── dijkstra.py
│   ├── euclerian_check.py
│   ├── floyd_warshall.py
│   ├── kruskal_mst.py
│   └── tarjan.py
├── part3/                          # Análises da parte 3
│   ├── power_law.py                # Verificação da Lei de Potência (Log-Log)
│   ├── robustness_analysis.py      # Simulações de falhas aleatórias e ataques (Boxplots)
│   └── small_world_metrics.py      # Cálculo das propriedades Small-World
├── wikispeedia_paths-and-graph/    # Arquivos do dataset
│   ├── articles.tsv                # Vértices do grafo
│   └── links.tsv                   # Arestas do grafo
├── directed_graph.py               # Classe principal do grafo e métodos da parte 1
├── graph_loader.py                 # Carregamento do grafo
├── utils.py                        # Funções auxiliares
└── main.py                         # Arquivo principal 
```

## Pré-requisitos e Dependências

O projeto foi desenvolvido em **Python 3.x**. A grande maioria da lógica utiliza as bibliotecas padrão do Python (como `math`, `random`, `collections` e `heapq`). As dependências externas são estritamente utilizadas para **visualização de dados e plotagem gráfica**.

Bibliotecas necessárias:
* `matplotlib` (Geração de histogramas, boxplots e gráficos log-log)
* `networkx` (Exclusivamente para o layout e plotagem visual da amostra do grafo)

## Como Configurar e Rodar o Projeto

Siga as instruções abaixo para reproduzir o ambiente e executar as análises localmente.

### 1. Clonar o repositório
```bash
git clone git@github.com:biaespinheira/TP-MATA53.git
cd TP-MATA53-main
```

### 2. Preparar o Dataset
Certifique-se de que os arquivos extraídos do dataset oficial do SNAP (`articles.tsv` e `links.tsv`) estejam localizados exatamente dentro da pasta `wikispeedia_paths-and-graph/` na raiz do projeto.

### 3. Configurar o Ambiente Virtual 
Para isolar as dependências, ative um ambiente virtual:

**No Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**No Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar as Dependências
Com o ambiente ativado, instale todos os pacotes necessários utilizando o arquivo de requisitos:

```bash
pip install -r requirements.txt
```

### 5. Executar a Bateria de Testes
O arquivo `main.py` funciona como o grande maestro da aplicação. Ele executará sequencialmente a Parte I, Parte II e Parte III, imprimindo os resultados direto no terminal.

```bash
python main.py
```

> Durante a execução, o código fará pausas para exibir os gráficos no `matplotlib` (Histogramas, Grafo em Teia, Lei de Potência e Boxplots de Robustez). **O terminal só continuará a execução e os cálculos da próxima etapa após a janela do gráfico atual ser fechada.**
