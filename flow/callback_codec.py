import ast
from decimal import Decimal

CB_DELIMITER = '|'


class CallbackCodec:

    encode_rules = {
        'person_id': int,
        'participant_id': int,
        'coeff': str,
        'payment': str
    }

    decode_rules = {
        'person_id': int,
        'participant_id': int,
        'coeff': Decimal,
        'payment': Decimal
    }

    @staticmethod
    def encode_stage(stage: 'Stage') -> str:
        return stage.name

    @staticmethod
    def _cast(data: dict, rules: dict) -> dict:
        new_data = dict()
        for key, value in data.items():
            if key in rules and value is not None:
                new_data[key] = rules[key](value)
            else:
                new_data[key] = value
        return new_data

    @classmethod
    def encode_payload(cls, data: dict):
        return str(cls._cast(data, cls.encode_rules))

    @classmethod
    def decode_payload(cls, data: str) -> dict:
        return cls._cast(ast.literal_eval(data), cls.decode_rules)
