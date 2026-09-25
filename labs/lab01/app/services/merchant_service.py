# ЛР1: сервис магазина и привязка объектов к API.
from app.support.types import CheckResult, Repository
from app.support.errors import DomainError
from app.domain.merchant import Merchant


class MerchantService:
    def __init__(self, repository, rules=()):
        self._repository = repository

    def register(self, entity):
        return self._repository.add(entity)

    def get(self, key):
        return self._repository.get(key)

    def suspend(self, key):
        self.get(key).suspend()

    def activate(self, key):
        self.get(key).activate()

    def close(self, key):
        self.get(key).close()

    def check(self, key, context):
        entity = self.get(key)
        result = entity.availability()
        if not result.allowed:
            return result
        if entity.category == "GAMBLING":
            return CheckResult(False, "MERCHANT_CATEGORY_DENIED")
        if context.channel not in {"POS", "ONLINE"}:
            return CheckResult(False, "MERCHANT_CHANNEL_DENIED")
        return CheckResult(True)


def make_entity(merchant_id, name, category, country):
    return Merchant(merchant_id, name, category, country)


def view(entity):
    return {
        "merchant_id": entity.merchant_id,
        "name": entity.name,
        "category": entity.category,
        "country": entity.country,
        "status": entity.status,
    }


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def new_service(repository=None):
    if repository is None:
        repository = Repository("merchant_id")
    return MerchantService(repository)