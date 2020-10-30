from abc import ABC, abstractmethod

class ObservableEngine(Engine):
    def __init__(self): 
        self.__subscribers = set()     

    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber) 
    
    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber) # Удаление подписчика из списка
        
    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)
    
class AbstractObserver(ABC):
    @abstractmethod
    def update():
        pass

class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message['title'])
    
class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = []

    def update(self, message):
        find = False
        for i in self.achievements:
            if i['title'] == message['title']:
                find = True
        if find == False:
            self.achievements.append(message)
