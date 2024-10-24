import os
import json

class Validator:
    def __init__(self):
        # Define the path to the schema file
        self.schema_path = os.path.join(os.path.dirname(__file__), "data/schema.json")
        self.schema = self.load_schema()

    def load_schema(self):
        """Load the JSON schema from the specified path."""
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        with open(self.schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def validate(self, data):
        """Validate the given data against the schema."""
        from jsonschema import validate, ValidationError

        try:
            validate(instance=data, schema=self.schema)
            return True, "Validation successful."
        except ValidationError as e:
            return False, f"Validation error: {e.message}"
        except Exception as e:
            return False, f"Unexpected error during validation: {str(e)}"
