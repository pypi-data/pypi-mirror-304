from typing import List, Optional


class FeaturesParams:
    def __init__(self, geom_group, behaviour_group, volume_name,
                 settings4geom, settings4behaviour, settings4volume):
        self.geom_group: List[str] = geom_group
        self.behaviour_group: List[str] = behaviour_group
        self.volume_name: str = volume_name
        self.settings4geom: Optional[List] = settings4geom
        self.settings4behaviour: Optional[List] = settings4behaviour
        self.settings4volume: Optional[List] = settings4volume
