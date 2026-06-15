from dataclasses import dataclass
from html import escape

from flow.stages import Stage


@dataclass
class Menu:
    """Граф переходов"""

    start_stage: Stage
    stages: tuple[Stage, ...] = tuple()

    def get_stage_by_name(self, name: str) -> Stage | None:
        for stage in self.stages:
            if stage.name == name:
                return stage
        return None

    def html_escape(self):
        for stage in self.stages:
            stage.title = escape(stage.title)
            stage.text = escape(stage.text)
