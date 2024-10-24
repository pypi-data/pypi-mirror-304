import os
import json

class Validator:
    def __init__(self, template_id: int):
        # テンプレートIDに基づいて適切なスキーマパスを設定
        self.schema_path = os.path.join(
            os.path.dirname(__file__), "templates", f"m{template_id}_s.json"
        )
        self.schema = self.load_schema()

    def load_schema(self):
        """指定されたスキーマをロードします。"""
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        
        with open(self.schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate(self, data):
        """JSONデータがスキーマに準拠しているか検証します。"""
        from jsonschema import validate, ValidationError

        try:
            validate(instance=data, schema=self.schema)
            return True, "Validation successful"
        except ValidationError as e:
            return False, f"Validation failed: {e.message}"
