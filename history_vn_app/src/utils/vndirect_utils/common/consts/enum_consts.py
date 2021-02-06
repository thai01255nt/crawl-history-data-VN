class IndexSymbol:
    VNDIRECT = 'VNDIRECT'
    HNX = 'HNX'
    VN30 = 'VN30'

    @staticmethod
    def __all_values__():
        return [getattr(IndexSymbol, attr) for attr in dir(IndexSymbol) if not attr.startswith('__')]

    @staticmethod
    def __all_keys__():
        return [getattr(IndexSymbol, attr) for attr in dir(IndexSymbol) if not attr.startswith('__')]
