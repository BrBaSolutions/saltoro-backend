from src.strategies.dto.request.strategy import StrategyDetails, StrategyCreate
from src.strategies.entities.strategy import Strategy


class StrategyMapper:
    @staticmethod
    def strategy_entity_to_dto(
            strategy: Strategy,
            asset_url: str
    ) -> StrategyDetails:
        return StrategyDetails(
            asset_url=asset_url,
            **strategy.__dict__
        )

    @staticmethod
    def strategy_dto_to_entity(
            strategy: StrategyCreate
    ) -> Strategy:
        return Strategy(
            **strategy.model_dump(exclude=["file_name"])
        )
