from decimal import Decimal, InvalidOperation


class BaseValidator:
    def validate(self, value: object) -> object:
        return value


class NonEmptyStringValidator(BaseValidator):
    def validate(self, value: object) -> str:
        result = str(value).strip()
        if not result:
            raise ValueError("Пустая строка недопустима")
        return result


class FloatValidator(BaseValidator):
    def validate(self, value: object) -> float:
        normalized = str(value).strip().replace(",", ".")
        try:
            return float(normalized)
        except ValueError as exc:
            raise ValueError("Введите корректное число") from exc


class PositiveFloatValidator(FloatValidator):
    def validate(self, value: object) -> float:
        result = super().validate(value)
        if result <= 0:
            raise ValueError("Введите число больше нуля")
        return result


class DecimalValidator(BaseValidator):
    def validate(self, value: object) -> Decimal:
        normalized = str(value).strip().replace(",", ".")
        try:
            return Decimal(normalized)
        except InvalidOperation as exc:
            raise ValueError("Введите корректное число") from exc


class NonNegativeDecimalValidator(DecimalValidator):
    def validate(self, value: object) -> Decimal:
        result = super().validate(value)
        if result < 0:
            raise ValueError("Введите число не меньше нуля")
        return result
