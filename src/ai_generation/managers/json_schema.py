from functools import lru_cache
from pathlib import Path


class JsonSchemaManager:
    def __init__(self, shema_dir: str = r"data\bpmn_schemas"):
        self.shema_dir = Path(shema_dir)

    @lru_cache(maxsize=16)
    def get_schema(self, shema_name) -> None:
        file_path = self.shema_dir / f"{shema_name}.json"
        with open(file_path, "r") as f:
            schema = f.read()
        return schema


shema_manager = JsonSchemaManager()


def get_json_schema_namager() -> JsonSchemaManager:
    return shema_manager
