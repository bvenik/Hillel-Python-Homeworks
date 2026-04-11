class InsufficientResources(Exception):
    def __init__(self, required_resource: str, required_amount: int | float, current_amount: int| float) -> None:
        self.required_resource = required_resource
        self.required_amount = required_amount
        self.current_amount = current_amount
def execute(required_resource: str, required_amount: int | float, current_amount: int | float) -> None:
    if current_amount < required_amount:
        raise InsufficientResources(required_resource, required_amount, current_amount)
    else:
        print(f"You successfully bought {required_resource}. You lost {required_amount}. Your current amount is {current_amount - required_amount}.")

try:
    execute('apple', 100, 20)
except InsufficientResources as e:
    remain_amount = e.required_amount - e.current_amount
    print(f"You didn't bought {e.required_resource}. Your current amount is {e.current_amount}, but you need {remain_amount} more.")
execute('banana', 300, 1000)