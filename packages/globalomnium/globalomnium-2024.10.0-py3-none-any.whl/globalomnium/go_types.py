from dataclasses import dataclass, field

from datetime import datetime

from typing import List, Dict

@dataclass
class PeriodValue:
    start: datetime
    end: datetime
    value: float


@dataclass
class ConsumptionForPeriod(PeriodValue):
    pass
    # desglosed: Dict[str, float] = field(default_factory=dict)


@dataclass
class HistoricalConsumption:
    consumptions: List[ConsumptionForPeriod] = field(default_factory=list)
    total: float = 0
    # desglosed: Dict[str, float] = field(default_factory=dict)
