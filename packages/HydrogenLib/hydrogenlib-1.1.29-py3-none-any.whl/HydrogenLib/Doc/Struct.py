from ..Decorators import singleton_decorator, Instance


@Instance
@singleton_decorator
class CodeStruct:
    """
    你可以使用这个类来分离不同的代码部分
    with CodeStruct("Init"):
        # codes
        ...

    这个类没有任何实际操作，仅用于代码标记
    """

    def __init__(self, *args, **kwargs):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
