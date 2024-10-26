from typing import Optional, Dict, Any


def extract_feature_settings(features_settings, feature: str) -> Optional[Dict[str, Any]]:
    """
    Извлекает настройки для указанной фичи из конфигурации настроек фич.

    :param features_settings: Объект настроек фич, содержащий настройки для различных типов фич.
    :param feature: Имя фичи, для которой нужно извлечь настройки.
    :return: Словарь настроек для фичи, если фича найдена; иначе None.
    """
    if feature == features_settings.volume_name:
        return features_settings.settings4volume
    elif feature in features_settings.geom_group:
        return features_settings.settings4geom
    elif feature in features_settings.behaviour_group:
        return features_settings.settings4behaviour
    return None
