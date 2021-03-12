from internal.src.utils.history_utils.common.consts.enum_consts import IndexSymbol
from internal.src.utils.history_utils.common.consts.message_consts import IndexMessageConsts


class IndexUtils:
    @staticmethod
    def validate_index_symbol(index_symbol):
        if index_symbol not in IndexSymbol.__all_keys__():
            raise Exception(IndexMessageConsts.SYMBOL_NOT_EXISTS)
        return
