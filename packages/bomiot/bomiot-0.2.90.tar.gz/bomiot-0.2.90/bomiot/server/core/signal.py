from django.dispatch import Signal, receiver

my_signal = Signal(providing_args=['msg'])


@receiver(my_signal)
def my_signal_callback(sender, **kwargs):
    print(kwargs['msg'])  # 打印Hello world!