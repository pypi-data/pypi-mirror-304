from django.dispatch import Signal, receiver

my_signal = Signal()



class DataReturn:
    def __init__(self):
        self.data = None

    def get_data(self, sender, data):
        print(sender, data)

    @receiver(my_signal)
    def my_signal_callback(self, sender, **kwargs):
        self.get_data(sender, **kwargs)

