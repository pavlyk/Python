class Value:
    def __init__(self):
        self.amount = None
    def __get__(self, obj, obj_type):
        return obj.__dict__['amount']
    def __set__(self, obj, value):
        # self.amount = value*(1 - obj.commission)
        # self.amount - применит к всему классу Value
        # obj.__dict__['amount'] - применит к конкретному экземпляру Account
        # Происходит зацикливание!!!!!
        # obj.amount = value*(1 - obj.commission)
        # !!!!! Происходит зацикливание
        obj.__dict__['amount'] = value*(1 - obj.commission)
        a = 0

class Account:
    amount = Value() # дескриптор определен до __init__

    def __init__(self, commission):
        self.commission = commission

new_account = Account(0.1)
new_account.amount = 100

new_account2 = Account(0.2)
new_account2.amount = 300
print(new_account.amount, new_account2.amount)

# class Value:
#     def __init__(self):
#         self.amount = 0

#     def __get__(self, obj, obj_type):
#         return self.amount

#     def __set__(self, obj, value):
#         self.amount = value - value * obj.commission