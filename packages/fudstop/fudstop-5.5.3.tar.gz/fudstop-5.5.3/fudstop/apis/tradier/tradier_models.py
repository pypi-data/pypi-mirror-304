import pandas as pd



class Orders:
    def __init__(self, order):


        self.id = order.get('id')
        self.type = order.get('type')
        self.symbol = order.get('symbol')
        self.side = order.get('side')
        self.quantity = order.get('quantity')
        self.status = order.get('status')
        self.duration = order.get('duration')
        self.price = order.get('price')
        self.avg_fill_price = order.get('avg_fill_price')
        self.exec_quantity = order.get('exec_quantity')
        self.last_fill_price = order.get('last_fill_price')
        self.last_fill_quantity = order.get('last_fill_quantity')
        self.remaining_quantity = order.get('remaining_quantity')
        self.create_date = order.get('create_date')
        self.transaction_date = order.get('transaction_date')
        self._class = order.get('class')


        self.dict = { 
            'id': self.id,
            'type': self.type,
            'ticker': self.symbol,
            'side': self.side,
            'quantity': self.quantity,
            'status': self.status,
            'duration': self.duration,
            'price': self.price,
            'avg_fill_price': self.avg_fill_price,
            'last_fill_price': self.last_fill_price,
            'last_fill_quantity': self.last_fill_quantity,
            'remaining_quantity': self.remaining_quantity,
            'create_date': self.create_date,
            'transaction_date': self.transaction_date,
            'class': self._class
        }


        self.discord_dict = { 
            'ticker': self.symbol,
            'type': self.type,
            'side': self.side,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.transaction_date,
            
            
        }
        #self.as_discord_dataframe = pd.DataFrame(self.discord_dict)
        self.as_dataframe = pd.DataFrame(self.dict, index=[0])



class Balances:
    def __init__(self, balances):
        self.option_short_value = balances.get('option_short_value')
        self.total_equity = balances.get('total_equity')
        self.account_number = balances.get('account_number')
        self.account_type = balances.get('account_type')
        self.close_pl = balances.get('close_pl')
        self.current_requirement = balances.get('current_requirement')
        self.equity = balances.get('equity')
        self.long_market_value = balances.get('long_market_value')
        self.market_value = balances.get('market_value')
        self.open_pl = balances.get('open_pl')
        self.option_long_value = balances.get('option_long_value')
        self.option_requirement = balances.get('option_requirement')
        self.pending_orders_count = balances.get('pending_orders_count')
        self.short_market_value = balances.get('short_market_value')
        self.stock_long_value = balances.get('stock_long_value')
        self.total_cash = balances.get('total_cash')
        self.uncleared_funds = balances.get('uncleared_funds')
        self.pending_cash = balances.get('pending_cash')
        self.margin = balances.get('margin')

        self.dict = {
            'option_short_value': self.option_short_value,
            'total_equity': self.total_equity,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'close_pl': self.close_pl,
            'current_requirement': self.current_requirement,
            'equity': self.equity,
            'long_market_value': self.long_market_value,
            'market_value': self.market_value,
            'open_pl': self.open_pl,
            'option_long_value': self.option_long_value,
            'option_requirement': self.option_requirement,
            'pending_orders_count': self.pending_orders_count,
            'short_market_value': self.short_market_value,
            'stock_long_value': self.stock_long_value,
            'total_cash': self.total_cash,
            'uncleared_funds': self.uncleared_funds,
            'pending_cash': self.pending_cash,
            'margin': self.margin
        }

        self.as_dataframe = pd.DataFrame(self.dict)