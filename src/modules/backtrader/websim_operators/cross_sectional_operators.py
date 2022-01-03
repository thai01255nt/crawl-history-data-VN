import numpy as np

from src.modules.backtrader.websim_operators.utils import WebsimOperatorUtils


class CrossSectionalOperators:
    @staticmethod
    def rank(x: np.ndarray, rate: int = 2) -> np.ndarray:
        WebsimOperatorUtils.validate_dimension(data=x, ndim=2)
        temp = x.argsort(axis=1)
        flat_size = x.shape[0] * x.shape[1]
        temp.resize(flat_size)
        flat_row_index = np.repeat(np.arange(x.shape[0]), x.shape[1], axis=0)
        flat_col_index = np.tile(np.arange(x.shape[1]), x.shape[0])
        ranks = np.empty_like(x)
        ranks[flat_row_index, temp] = flat_col_index
        ranks = ranks / x.shape[1]
        ranks = ranks.round(rate)
        return ranks
