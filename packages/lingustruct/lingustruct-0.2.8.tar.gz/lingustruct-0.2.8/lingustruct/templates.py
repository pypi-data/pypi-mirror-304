import json
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

def load_template(template_name: str) -> dict:
    """
    指定されたテンプレート名のJSONファイルをロードする。
    
    Args:
        template_name (str): ロードするテンプレートの名前（拡張子なし）。
    
    Returns:
        dict: テンプレートの内容。
    
    Raises:
        FileNotFoundError: テンプレートファイルが存在しない場合。
        json.JSONDecodeError: JSONのパースに失敗した場合。
    """
    file_path = os.path.join(TEMPLATE_DIR, f"{template_name}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{template_name}.json が見つかりません。")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

class TemplateManager:
    def __init__(self, data_path='lingustruct/data/data.json'):
        self.data_path = data_path
        self.templates = self.load_templates()

    def load_templates(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"{self.data_path} が見つかりません。")
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('fields', [])

    def get_field(self, field_name):
        for field in self.templates:
            if field['name'] == field_name:
                return field
        return None

    def add_field(self, field):
        self.templates.append(field)
        self.save_templates()

    def save_templates(self):
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump({"fields": self.templates}, f, ensure_ascii=False, indent=4)
