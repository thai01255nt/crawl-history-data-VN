import numpy as np

from src.modules.backtrader.websim_operators import CrossSectionalOperators
from src.modules.backtrader.websim_operators.utils import WebsimOperatorUtils


class SettingOperators:
    @staticmethod
    def universe(volumes: np.ndarray, universes: np.ndarray):
        round_rate = round(np.log10(volumes.shape[1]))
        WebsimOperatorUtils.validate_dimension(data=volumes, ndim=2)
        WebsimOperatorUtils.validate_dimension(data=universes, ndim=2)
        if volumes.shape[0] != universes.shape[0]:
            raise Exception(f"Miss match {volumes.shape} volume and {len(universes)} universes")
        rank_volumes = CrossSectionalOperators.rank(x=volumes, rate=round_rate)
        universe_thresh_hold = (universes / volumes.shape[1]).round(round_rate)
        return rank_volumes < universe_thresh_hold

    @staticmethod
    def neutralize(alpha: np.ndarray):
        WebsimOperatorUtils.validate_dimension(data=alpha, ndim=1)
        removed_nan_alpha = alpha[~np.isnan(alpha)]
        sum_alpha = removed_nan_alpha.sum()
        alpha = (alpha - sum_alpha / removed_nan_alpha.shape[0]) / sum_alpha
        removed_nan_alpha = alpha[~np.isnan(alpha)]
        alpha = alpha / (removed_nan_alpha * (~(removed_nan_alpha < 0)).astype(int)).sum()
        return alpha
