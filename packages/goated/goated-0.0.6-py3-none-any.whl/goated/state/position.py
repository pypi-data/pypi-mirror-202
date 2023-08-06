from decimal import Decimal
from typing import List
import json
import time
from datetime import datetime

class Position():
    
    def __init__(
        self,
        probability_price: Decimal,
        decimal_price: Decimal,
        american_price: Decimal,
        payout: Decimal,
        stake: Decimal,
    ):
        self.probability_price = probability_price
        self.decimal_price = decimal_price
        self.american_price = american_price
        self.payout = payout
        self.stake = stake

    def serialize_to_dict(
        self,
    ):
        d = {
            'probability_price': f'{self.probability_price:.18f}',
            'decimal_price': f'{self.probability_price:.18f}',
            'american_price': f'{self.probability_price:.18f}',
            'payout': f'{self.payout:.18f}',
            'stake': f'{self.stake:.18f}',
        }
        return d

    def serialize_to_json(
        self,
        indent: int = 0
    ):
        return json.dumps(
            self.serialize_to_dict(),
            indent=indent
        )

class SelectionPosition():

    def __init__(
        self,
        state,
        market_id: int,
        selection_id: int,
        net_payout: Decimal,
        net_stake: Decimal,
        buys: List[Position],
        sells: List[Position],
        _update_timestamp: datetime = None
    ):
        self.state = state
        self.market_id = market_id
        self.selection_id = selection_id
        self.net_payout = net_payout
        self.net_stake = net_stake
        self.buys = buys
        self.sells = sells
        self._update_timestamp = _update_timestamp if _update_timestamp else datetime.utcnow()

    @property
    def probability_price(
        self,
    ):
        return self.net_stake / self.net_payout if self.net_payout != Decimal(0) else None

    @classmethod
    def load_from_json(
        cls,
        state,
        data: str,
    ):
        if type(data) == str:
            data = json.loads(data)
        return cls(
            state = state,
            market_id = data.get('market'),
            selection_id = data.get('id'),
            net_stake = Decimal(data.get('net_stake')),
            net_payout = Decimal(data.get('net_payout')),
            buys = [
                Position(
                    probability_price = Decimal(p.get('probability_price')),
                    decimal_price = Decimal(p.get('decimal_price')),
                    american_price = Decimal(p.get('american_price')),
                    payout = Decimal(p.get('payout')),
                    stake = Decimal(p.get('stake'))
                )
                for p in data.get('buys')
            ],
            sells = [
                Position(
                    probability_price = Decimal(p.get('probability_price')),
                    decimal_price = Decimal(p.get('decimal_price')),
                    american_price = Decimal(p.get('american_price')),
                    payout = Decimal(p.get('payout')),
                    stake = Decimal(p.get('stake'))
                )
                for p in data.get('sells')
            ],
            _update_timestamp = datetime.strptime(data.get('_update_timestamp'), "%Y-%m-%dT%H:%M:%SZ") if data.get('_update_timestamp') != None else None,
        )
        
    def serialize_to_dict(
        self,
    ):
        d = {
            'id': self.selection_id,
            'market': self.market_id,
            'net_stake': f'{self.net_stake:18f}',
            'net_payout': f'{self.net_payout:18f}',
            'buys': [
                b.serialize_to_dict()
                for b in self.buys
            ],
            'sells': [
                s.serialize_to_dict()
                for s in self.sells
            ],
            '_update_timestamp': self._update_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ") if self._update_timestamp else None,
        }
        return d

    def serialize_to_json(
        self,
        indent: int = 0
    ):
        return json.dumps(
            self.serialize_to_dict(),
            indent=indent
        )


    @property
    def selection(self):
        return self.state.selections.get(
            self.selection_id
        )
    
    @property
    def market(self):
        if self.selection:
            return self.selection.market
        return None

    @property
    def pool(self):
        if self.market:
            return self.market.pool
        return None

    
    def __repr__(self):
        return f"<Position: {self.market_id} {self.selection_id} | S: {self.net_stake:.2f} / P: {self.net_payout:.3f} >"

    def __str__(self):
        return f"<Position: {self.market_id} {self.selection_id} | S: {self.net_stake:.2f} / P: {self.net_payout:.3f} >"

