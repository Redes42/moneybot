import ast

CB_DELIMITER = '|'

class CallbackCodec:

    @staticmethod
    def encode_stage(stage: 'Stage', payload: dict | None = None) -> str:
        return f'{stage.name}{CB_DELIMITER}{str(payload)}' if payload  else f'{stage.name}'

    @staticmethod
    def decode(data: str) -> tuple[str, dict | None]:
        stage_name, sep, payload = data.partition(CB_DELIMITER)
        if payload:
            payload = ast.literal_eval(payload)
        return stage_name, payload
