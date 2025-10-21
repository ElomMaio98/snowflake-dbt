import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.snowflake_connection import SnowflakeConnection
from common.api_client import CoinGeckoClient


class TestConnections:
    """Suite de testes para todas as conexões"""
    
    def __init__(self):
        self.snowflake = SnowflakeConnection()
        self.coingecko = CoinGeckoClient()

    def test_snowflake_connection(self) -> bool:
        """Testa conexão com Snowflake"""
        print("\nTestando conexão Snowflake...")
        print("-" * 60)
        
        try: 
            with self.snowflake as sf:
                # Versão
                version = sf.execute_query("SELECT CURRENT_VERSION()")[0][0]
                print(f"Conexão bem-sucedida!")
                print(f"Versão Snowflake: {version}")

                # Usuário
                user = sf.execute_query("SELECT CURRENT_USER()")[0][0]
                print(f"Conectado como: {user}")
                
                # Database
                database = sf.execute_query("SELECT CURRENT_DATABASE()")[0][0]
                print(f"Database: {database}")
             
                # Schema
                schema = sf.execute_query("SELECT CURRENT_SCHEMA()")[0][0]
                print(f"Schema: {schema}")

                # Warehouse
                warehouse = sf.execute_query("SELECT CURRENT_WAREHOUSE()")[0][0]
                print(f"Warehouse: {warehouse}")

                # Tabelas
                tables = sf.execute_query("SHOW TABLES IN SCHEMA raw")
                print(f"Encontradas {len(tables)} tabelas no schema raw:")
                for table in tables:
                    print(f"   - {table[1]}")

                # Conta registros
                market_count = sf.execute_query("SELECT COUNT(*) FROM raw.market_data")[0][0]
                history_count = sf.execute_query("SELECT COUNT(*) FROM raw.price_history")[0][0]
                print(f"\nRegistros atuais:")
                print(f"   - market_data: {market_count} registros")
                print(f"   - price_history: {history_count} registros")
                
                print("-" * 60)
                print("Teste Snowflake PASSOU")
                return True  # ← IMPORTANTE!
                
        except ConnectionError as e:
            print(f"Erro de conexão!{e}")
        except ValueError as e:
            print(f"Valor inválido!{e}")
        except Exception as e:
            print(f"Outro erro! {e}")        
            return False
        
    def test_coingecko_api(self) -> bool:
        """Testa API do CoinGecko"""
        print("\nTestando API CoinGecko...")
        print("-" * 60)
        
        try:
            # Ping
            if not self.coingecko.ping():
                raise Exception("Ping falhou")
            print("Ping com sucesso")
            
            # Get market data
            data = self.coingecko.get_market_data(vs_currency='brl', per_page=5)
            if not data:
                raise Exception("Não conseguimos obter dados de mercado")
            print(f"Dados obtidos: {len(data)} moedas")
            
            # Get price history
            history = self.coingecko.get_price_history('bitcoin', Days=7)  # ← CORRIGIDO!
            if not history:
                raise Exception("Não conseguimos obter histórico de preços")
            print(f"Histórico obtido: {len(history.get('prices', []))} pontos")
            
            print("-" * 60)
            print("Teste CoinGecko API PASSOU")
            return True
            
        except Exception as e:
            print(f"Teste CoinGecko API FALHOU: {e}")
            print("\nTroubleshooting:")
            print("   1. Verifica conexão com internet")
            print("   2. Verifica se CoinGecko API não está fora do ar")
            print("   3. Verifica se não atingiu rate limit")
            print("   4. Confirma que BASE_URL está no .env")
            print("-" * 60)
            return False
    
    def run_all_tests(self) -> bool:
        print("=" * 60)
        print("CRYPTO ANALYTICS - TESTES DE CONEXÃO")
        print("=" * 60)
        
        snowflake_ok = self.test_snowflake_connection()
        coingecko_ok = self.test_coingecko_api()
        
        print("\n" + "=" * 60)
        print("RESUMO DOS TESTES")
        print("=" * 60)
        print(f"Snowflake:   {'PASSOU' if snowflake_ok else 'FALHOU'}")
        print(f"CoinGecko:   {'PASSOU' if coingecko_ok else 'FALHOU'}")
        print("=" * 60)
        
        all_passed = snowflake_ok and coingecko_ok
        
        if all_passed:
            print("\nTodos os testes PASSARAM!")
        else:
            print("\nAlguns testes FALHARAM.")
        
        print("=" * 60)
        return all_passed


def main():
    tester = TestConnections()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()