# KIS Trading Skill

## Tools

### get_my_portfolio
내 계좌의 잔고와 보유 종목 리스트를 조회합니다.
**Command:**
python C:/Users/nembi/.openclaw/scripts/kis_trade.py balance

### get_stock_price
특정 종목의 현재가를 조회합니다.
- `symbol` (string): 6자리 종목코드
**Command:**
python C:/Users/nembi/.openclaw/scripts/kis_trade.py price {{symbol}}

### execute_order
주식을 매수하거나 매도합니다. (주의: 실제 주문이 나갑니다)
- `symbol` (string): 종목코드
- `qty` (number): 수량
- `price` (number): 가격 (0이면 시장가 주문이나, API 설정에 따라 다를 수 있음)
- `side` (string): 'BUY' 또는 'SELL'
**Command:**
python C:/Users/nembi/.openclaw/scripts/kis_trade.py order {{symbol}} {{qty}} {{price}} {{side}}