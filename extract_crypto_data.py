import sys
from datetime import datetime
from common.snowflake_connection import SnowflakeConnection
from common.api_client import CoinGeckoClient

def extract_market_data(api: CoinGeckoClient, num_coins: int=50):
    data =  api.get_market_data(vs_currency='brl', per_page=num_coins)
    return data

def load_market_data(sf: SnowflakeConnection, data: list):
    now = datetime.now()
    inserted = 0
    for coin in data:
        try:
            values = {
                'id': coin.get('id', ''),
                'symbol': coin.get('symbol', ''),
                'name': coin.get('name', ''),
                'current_price': coin.get('current_price', 0) or 0,
                'market_cap': coin.get('market_cap', 0) or 0,
                'market_cap_rank': coin.get('market_cap_rank', 0) or 0,
                'total_volume': coin.get('total_volume', 0) or 0,
                'high_24h': coin.get('high_24h', 0) or 0,
                'low_24h': coin.get('low_24h', 0) or 0,
                'price_change_24h': coin.get('price_change_24h', 0) or 0,
                'price_change_percentage_24h': coin.get('price_change_percentage_24h', 0) or 0,
                'price_change_percentage_7d': coin.get('price_change_percentage_7d_in_currency', 0) or 0,
                'price_change_percentage_30d': coin.get('price_change_percentage_30d_in_currency', 0) or 0,
                'circulating_supply': coin.get('circulating_supply', 0) or 0,
                'total_supply': coin.get('total_supply', 0) or 0,
                'max_supply': coin.get('max_supply', 0) or 0,
                'ath': coin.get('ath', 0) or 0,
                'ath_date': coin.get('ath_date', now),
                'atl': coin.get('atl', 0) or 0,
                'atl_date': coin.get('atl_date', now),
                'last_updated': coin.get('last_updated', now),
                'extracted_at': now
            }
            sql = f"""
                INSERT INTO raw.market_data VALUES (
                    '{values['id']}',
                    '{values['symbol']}',
                    '{values['name']}',
                    {values['current_price']},
                    {values['market_cap']},
                    {values['market_cap_rank']},
                    {values['total_volume']},
                    {values['high_24h']},
                    {values['low_24h']},
                    {values['price_change_24h']},
                    {values['price_change_percentage_24h']},
                    {values['price_change_percentage_7d']},
                    {values['price_change_percentage_30d']},
                    {values['circulating_supply']},
                    {values['total_supply']},
                    {values['max_supply']},
                    {values['ath']},
                    '{values['ath_date']}',
                    {values['atl']},
                    '{values['atl_date']}',
                    '{values['last_updated']}',
                    '{values['extracted_at']}'
                )
            """
            
            sf.execute_query(sql)
            inserted += 1
            if inserted % 10 == 0:
                print(f"   Progresso: {inserted}/{len(data)} registros...")
                
        except Exception as e:
            print(f"Erro ao inserir {coin.get('name', 'Unknown')}: {e}")
            continue
    
    print(f"{inserted} registros inseridos com sucesso")
    return inserted

def main():
    try:
        api = CoinGeckoClient()
        market_data = extract_market_data(api, num_coins=50)
        with SnowflakeConnection() as sf:
            inserted = load_market_data(sf, market_data)
        print("\n" + "=" * 60)
        print("RESUMO DA EXECUÇÃO")
        print(f"Moedas extraídas: {len(market_data)}")
        print(f"Registros inseridos: {inserted}")
        print(f"Taxa de sucesso: {(inserted/len(market_data)*100):.1f}%")
        print("\nETL executado com sucesso!")
        print("\n" + "=" * 60)
        return 0
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERRO NA EXECUÇÃO DO ETL")
        print(f"Erro: {e}")
        print("\n" + "=" * 60)
        return 0
if __name__ == "__main__":
    sys.exit(main())