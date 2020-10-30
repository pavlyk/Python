# class SomeObject:
#     def __init__(self):
#         self.integer_field = 0
#         self.float_field = 0.0
#         self.string_field = ""


class EventGet:
    def __init__(self, kind):
        self.kind = kind
        self.type = 1


class EventSet:
    def __init__(self, kind):
        self.kind = kind
        self.type = 2


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event.kind, int) or event.kind == int:
            if event.type == 1:
                return obj.integer_field
            else:
                obj.integer_field = event.kind
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event.kind, float) or event.kind == float:
            if event.type == 1:
                return obj.float_field
            else:
                obj.float_field = event.kind
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event.kind, str) or event.kind == str:
            if event.type == 1:
                return obj.string_field
            else:
                obj.string_field = event.kind
        else:
            return super().handle(obj, event)

# obj = SomeObject()
# obj.integer_field = 42
# obj.float_field = 3.14
# obj.string_field = "some text"
# chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
# print(chain.handle(obj, EventGet(int)))
# print(chain.handle(obj, EventGet(float)))
# print(chain.handle(obj, EventGet(str)))