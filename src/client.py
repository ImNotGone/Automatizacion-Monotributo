
class Client:
    def __init__(self, id, earnings = 0, expenses = 0):
        self._id = id
        # me aseguro que los valores no sean negativos
        self._earnings = max(earnings, 0)
        self._expenses = max(expenses, 0)

    def __str__(self):
        return f"Client id:{self._id}, earnings:{self._earnings}, expenses:{self._expenses}"

    @property
    def id(self):
        return self._id

    @property
    def earnings(self):
        return self._earnings

    @property
    def expenses(self):
        return self._expenses

    @property
    def balance(self):
        return self._earnings - self._expenses

    def add_earnings(self, earnings):
        if earnings < 0:
            raise ValueError("Earnings cannot be negative")
        self._earnings += earnings

    def add_expenses(self, expenses):
        if expenses < 0:
            raise ValueError("Expenses cannot be negative")
        self._expenses += expenses
