from app.support.types import CheckResult, Repository
from app.support.types import name as valid_name, country as valid_country
from app.support.errors import DomainError


class Merchant:
    def __init__(self, merchant_id, name, category, country):
        self._merchant_id = merchant_id
        self._name = valid_name(name)
        self._category = category
        self._country = valid_country(country)
        self._status = "ACTIVE"

    @property
    def merchant_id(self):
        return self._merchant_id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def country(self):
        return self._country

    @property
    def status(self):
        return self._status

    def _transition_to(self, allowed_from, new_status):
        if self._status not in allowed_from:
            raise DomainError("INVALID_STATE")
        self._status = new_status

    def suspend(self):
        self._transition_to(("ACTIVE",), "SUSPENDED")

    def activate(self):
        self._transition_to(("SUSPENDED",), "ACTIVE")

    def close(self):
        self._transition_to(("ACTIVE", "SUSPENDED"), "CLOSED")

    def availability(self):
        if self._status == "ACTIVE":
            return CheckResult(True)
        return CheckResult(False, "MERCHANT_" + self._status)

    def rename(self, new_name):
        self._name = valid_name(new_name)

    def describe(self):
        return f"{self.merchant_id}:{self.name}:{self.category}:{self.status}"