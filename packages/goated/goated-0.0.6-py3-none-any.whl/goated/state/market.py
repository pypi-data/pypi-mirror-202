from typing import Union, List
import json
from decimal import Decimal
from datetime import datetime
from ..utils.converter import convert_to_probability
from ..utils.bucketing import DEFAULT_AMERICAN_SCHEMA, DEFAULT_DECIMAL_SCHEMA, DEFAULT_PROBABILITY_SCHEMA
import time

class Market():

    def __init__(
        self,
        state,
        id: int,
        event_id: int,
        currency: str,
        pool_id: int,
        expiry_time: datetime,
        status: str,
        is_main_market: bool, 
        handicap: Union[Decimal, None],
        type_id: int,
        type_name: str,
        num_winners: int,
        num_selections: int,
        min_post_quantity: Decimal,
        supports_in_play: bool,
        in_play_delay_seconds: Decimal,
        is_cross_matching: bool,
        matched_volume: Decimal,
        available_volume: Decimal,
        terms: str,
        description: str,
        category_id: int,
        subcategory_id: int,
        payoff_signature_length: int,
        price_schema: str,
        _update_timestamp: datetime = None
    ):
        self.state = state
        self.id = id
        self.event_id = event_id 
        self.currency = currency 
        self.pool_id = pool_id
        self.expiry_time = expiry_time 
        self.status = status 
        self.is_main_market= is_main_market
        self.handicap = handicap 
        self.type_id = type_id 
        self.type_name = type_name
        self.num_winners = num_winners 
        self.num_selections= num_selections
        self.min_post_quantity = min_post_quantity 
        self.supports_in_play = supports_in_play 
        self.in_play_delay_seconds = in_play_delay_seconds 
        self.is_cross_matching = is_cross_matching 
        self.matched_volume= matched_volume
        self.available_volume= available_volume
        self.terms = terms
        self.description = description
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.payoff_signature_length = payoff_signature_length
        self._price_schema = price_schema
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
            event_id = data.get('event'),
            currency = data.get('currency'),
            pool_id = data.get('pool'),
            expiry_time = datetime.strptime(data.get('expiry_time_utc'), "%Y-%m-%dT%H:%M:%SZ") if data.get('expiry_time_utc') != None else None,
            status = data.get('status'),
            is_main_market = data.get('is_main_market'),
            handicap = data.get('handicap'),
            type_id = data.get('type').get('id') if data.get('type') else None,
            type_name = data.get('type').get('name') if data.get('type') else None,
            num_winners = data.get('num_winners'),
            num_selections = data.get('num_selections'),
            min_post_quantity = Decimal(data.get('min_post_quantity')) if data.get('min_post_quantity') != None else None,
            supports_in_play = data.get('supports_in_play'),
            in_play_delay_seconds = data.get('in_play_delay_seconds'),
            is_cross_matching = data.get('is_cross_matching'),
            matched_volume = Decimal(data.get('matched_volume')) if data.get('matched_volume') != None else None,
            available_volume = Decimal(data.get('available_volume')) if data.get('available_volume') != None else None,
            terms = data.get('terms'),
            description = data.get('description'),
            category_id = data.get('category'),
            subcategory_id = data.get('subcategory'),
            price_schema = data.get('price_schema'),
            payoff_signature_length = data.get('payoff_signature_length'),
            _update_timestamp = datetime.strptime(data.get('_update_timestamp'), "%Y-%m-%dT%H:%M:%SZ") if data.get('_update_timestamp') != None else None,
        )
        
    def serialize_to_dict(
        self,
    ):
        d = {
            'id': self.id,
            'event': self.event_id,
            'currency': self.currency,
            'pool': self.pool_id,
            'expiry_time_utc': self.expiry_time.strftime("%Y-%m-%dT%H:%M:%SZ") if self.expiry_time else None,
            'status': self.status,
            'is_main_market': self.is_main_market,
            'handicap': self.handicap,
            'type': {
                'id': self.type_id,
                'name': self.type_name
            } if self.type else None,
            'num_winners': self.num_winners,
            'num_selections': self.num_selections,
            'min_post_quantity': f'{self.min_post_quantity:.18f}',
            'supports_in_play': self.supports_in_play,
            'in_play_delay_seconds': self.in_play_delay_seconds,
            'is_cross_matching': self.is_cross_matching,
            'matched_volume': f'{self.matched_volume:.18f}' if self.matched_volume else None,
            'available_volume':  f'{self.available_volume:.18f}' if self.available_volume else None,
            'terms': self.terms,
            'description': self.description,
            'category': self.category_id,
            'subcategory': self.subcategory_id,
            'price_schema': self._price_schema,
            'payoff_signature_length': self.payoff_signature_length,
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
        market_data = state.client.get_markets(
            market_ids = [id]
        )[0]
        return cls.load_from_json(
            state = state,
            data = market_data
        )

    @property
    def pool(self):
        return self.state.pools.get(
            self.pool_id
        )

    @property
    def selections(self):
        return list(filter(
            lambda s: s.market_id == self.id,
            self.state.selections.values()
        ))
   
    @property
    def orders(self):
        return list(filter(
            lambda o: o.market_id == self.id,
            self.state.orders.values()
        ))

    @property
    def check_selections_complete(self):
        return (len(self.selections) == self.num_selections)

    @property
    def price_schema(self):
        if self._price_schema.upper() == 'DEFAULT_PROBABILITY_SCHEMA':
            return DEFAULT_PROBABILITY_SCHEMA
        elif self._price_schema.upper() == 'DEFAULT_DECIMAL_SCHEMA':
            return DEFAULT_DECIMAL_SCHEMA
        elif self._price_schema.upper() == 'DEFAULT_AMERICAN_SCHEMA':
            return DEFAULT_AMERICAN_SCHEMA
        else:
            raise Exception

    def __repr__(self):
        return f"<Market: {self.id}>"

    def __str__(self):
        return f"Market: {self.id}"

    
    