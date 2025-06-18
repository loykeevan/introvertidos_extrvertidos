from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[2]

PASTA_DADOS = PASTA_PROJETO / "dados"

# Caminho para os arquivos de dados de seu projeto
DADOS_ORIGINAIS = PASTA_DADOS / "personality_dataset.csv"

# Caminho para os arquivos de dados de seu projeto
DADOS_TRATADOS = PASTA_DADOS / "introvertido_extrovertido.parquet"

# Caminhos que você julgar necessário
PASTA_IMAGENS = PASTA_PROJETO / "imagens"
