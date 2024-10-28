from fastapi import FastAPI
from kiln_ai.utils.config import Config


def connect_settings(app: FastAPI):
    @app.post("/api/settings")
    def update_settings(new_settings: dict[str, int | float | str | bool | None]):
        Config.shared().update_settings(new_settings)
        return Config.shared().settings(hide_sensitive=True)

    @app.get("/api/settings")
    def read_settings():
        settings = Config.shared().settings(hide_sensitive=True)
        return settings

    @app.get("/api/settings/{item_id}")
    def read_item(item_id: str):
        settings = Config.shared().settings(hide_sensitive=True)
        return {item_id: settings.get(item_id, None)}
