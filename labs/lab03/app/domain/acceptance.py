from abc import ABC, abstractmethod
from app.support.types import CheckResult
from app.support.types import choice


class MerchantAcceptanceRule(ABC):
    @abstractmethod
    def check(self, entity, context):
        pass


class RestrictedCategoryRule(MerchantAcceptanceRule):
    def __init__(self, values):
        self._values = frozenset(values)
        for value in self._values:
            choice(value, ('GROCERY', 'RESTAURANT', 'FUEL', 'TRAVEL', 'GAMBLING', 'OTHER'), "INVALID_CONFIG")

    def check(self, entity, context):
        if entity.category in self._values:
            return CheckResult(False, "MERCHANT_CATEGORY_DENIED")
        return CheckResult(True)


class AcceptedChannelRule(MerchantAcceptanceRule):
    def __init__(self, values, code="MERCHANT_CHANNEL_DENIED"):
        self._values = frozenset(values)
        self._code = code
        for value in self._values:
            choice(value, ('POS', 'ONLINE'), "INVALID_CONFIG")

    def check(self, entity, context):
        if context.channel not in self._values:
            return CheckResult(False, self._code)
        return CheckResult(True)