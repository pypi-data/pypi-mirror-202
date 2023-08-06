from typing import Union, List
import json
from ..utils.payoff_signature import PayoffSignature
from decimal import Decimal
import time
from datetime import datetime

class Selection():

    def __init__(
        self,
        state,
        id: int,
        market_id: int,
        name: str,
        competitor: Union[dict, None],
        resolution_status: Union[str, None],
        payoff_signature: str,
        display_order: int,
        status: str,
        price_probability: str,
        _update_timestamp: datetime = None
    ):
        self.state = state
        self.id = id
        self.market_id = market_id
        self.name = name
        self.competitor = competitor
        self.resolution_status = resolution_status
        self.payoff_signature = PayoffSignature.from_string(payoff_signature)
        self.display_order = display_order
        self.status = status
        self.price_probability = Decimal(price_probability) if price_probability else Decimal(1)
        self._update_timestamp = _update_timestamp if _update_timestamp else datetime.utcnow()

    @classmethod
    def load_from_json(
        cls,
        state,
        data: Union[str, dict]
    ):
        if type(data) == str:
            data = json.loads(data)
        return cls(
            state = state,
            id = data.get('id'),
            market_id = data.get('market'),
            name = data.get('name'),
            competitor = data.get('competitor'),
            resolution_status = data.get('resolution_status'),
            payoff_signature = data.get('payoff_signature'),
            display_order = data.get('display_order'),
            status =data.get('status'),
            price_probability = data.get('price_probability'),
            _update_timestamp = datetime.strptime(data.get('_update_timestamp'), "%Y-%m-%dT%H:%M:%SZ") if data.get('_update_timestamp') != None else None,
        )
        
    def serialize_to_dict(
        self,
    ):
        d = {
            'id': self.id,
            'market': self.market_id,
            'name': self.name,
            'competitor': self.competitor,
            'resolution_status': self.resolution_status,
            'payoff_signature': self.payoff_signature.to_string(),
            'display_order': self.display_order,
            'status': self.status,
            'price_probability': self.price_probability,
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
    
        
    @classmethod
    def load_from_client(
        cls,
        state,
        id: int
    ):
        selection_data = state.client.get_selections(
            selection_ids = [id]
        )[0]
        return cls.load_from_json(
            state = state,
            data = selection_data
        )

    @property
    def market(self):
        return self.state.markets.get(
            self.market_id
        )

    @property
    def pool(self):
        if self.market:
            return self.market.pool
        return None

   
    @property
    def positions(self):
        return self.state.positions.get(
            self.id
        )

    @property
    def orders(self):
        
        return list(
            filter(
                lambda o: o.selection_id == self.id,
                self.state.orders.values()
            )
        )

    @property
    def fair_price(self):
        
        return self.price_probability/self.market.book_total if self.market.book_total else self.price_probability

    def __repr__(self):
        return f"<Selection: {self.id}>"

    def __str__(self):
        return f"<Selection: {self.id}>"
