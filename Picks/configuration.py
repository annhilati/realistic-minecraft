import logging
from pathlib import Path
from typing import Any
from pydantic import BaseModel, model_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)

logger = logging.getLogger(__name__)

class PickConfig(BaseSettings):

    tools: dict[
        str,                # tool type
        dict[               
            float,          # toughness (mining duration with hand)
            list[           
                str | dict[ # block id or block tag or 
                    str,        # block id or block tag
                    float       # vanilla hardness value
                ]
            ]
        ]
    ] = {}

    # Methode 1: Statischer Pfad mit pathlib.Path
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            TomlConfigSettingsSource(settings_cls),
            init_settings,
            env_settings,
        )

    @model_validator(mode='before')
    @classmethod
    def warn_on_extra_keys(cls, data: Any) -> Any:
        if isinstance(data, dict):
            known_keys = set(cls.model_fields.keys())
            provided_keys = set(data.keys())
            extra_keys = provided_keys - known_keys
            
            if extra_keys:
                logger.warning(
                    "Unerwartete Schlüssel in der Konfiguration gefunden (werden ignoriert): %s", 
                    ", ".join(extra_keys)
                )
        return data


    @classmethod
    def load_from_path(cls, config_path: Path) -> "PickConfig":
        """
        Erlaubt es, die Konfiguration beim Starten des Programms gezielt aus 
        einem bestimmten Path-Objekt zu laden.
        """
        # Wir zwingen die TOML-Source dazu, unsere übergebene Datei zu lesen
        toml_source = TomlConfigSettingsSource(cls, toml_file=config_path)
        
        # Pydantic-Settings priorisiert kwargs über alles andere.
        # Wir entpacken also die geparsten TOML-Daten als kwargs in die Klasse.
        return cls(**toml_source())
    
    
class ToolConfig(BaseModel):
    ...