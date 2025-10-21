# 🪙 Crypto Analytics - Pipeline ETL com dbt

Pipeline de dados end-to-end para análise de criptomoedas, extraindo dados da API CoinGecko e processando com dbt no Snowflake.

## 📊 Arquitetura
```
API CoinGecko → Python ETL → Snowflake (RAW) → dbt (Staging/Marts)
```

### Camadas de Dados:
- **RAW**: Dados brutos da API (50 criptomoedas)
- **STAGING**: Dados limpos e padronizados
- **MARTS**: Modelos analíticos (dimensões + fatos)

## 🛠️ Stack Tecnológica

- **Python 3.11+**: Extração e carga de dados
- **Snowflake**: Data warehouse
- **dbt Cloud**: Transformação de dados
- **CoinGecko API**: Fonte de dados de mercado

## 📁 Estrutura do Projeto
```
crypto-analytics/
├── python_etl/
│   ├── common/
│   │   ├── api_client.py          # Cliente CoinGecko
│   │   └── snowflake_connection.py # Conexão Snowflake
│   ├── tests/
│   │   └── test_integration.py    # Testes de integração
│   ├── extract_crypto_data.py     # Script principal ETL
│   └── requirements.txt
├── .env                            # Variáveis de ambiente
└── README.md
```

## 🚀 Como Executar

### 1. Configurar Ambiente
```bash
# Clonar repositório
git clone https://github.com/seu-usuario/crypto-analytics.git
cd crypto-analytics

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r python_etl/requirements.txt
```

### 2. Configurar .env
```env
SNOWFLAKE_ACCOUNT=sua_conta
SNOWFLAKE_USER=seu_usuario
SNOWFLAKE_PASSWORD=sua_senha
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_ROLE=
COINGECKO_API_KEY=
```

### 3. Executar ETL
```bash
cd python_etl
python extract_crypto_data.py
```

### 4. Executar dbt (dbt Cloud)
```bash
dbt run
dbt test
```

## 📊 Modelos dbt

### Staging
- **stg_market_data**: Limpeza e padronização dos dados brutos

### Marts
- **dim_coins**: Dimensão de moedas (atributos fixos)
- **fct_market_snapshot**: Fatos do mercado (métricas diárias)

## 📈 Métricas

- **50 criptomoedas** extraídas por execução
- **22 campos** por moeda
- **3 camadas** de processamento (RAW → Staging → Marts)
- **Taxa de sucesso**: 100%


## 👤 Autor

**Elom Nascimento**
- [LinkedIn]((https://www.linkedin.com/in/elom-maio))


## 📄 Licença

MIT License
