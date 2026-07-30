from pathlib import Path

from .csv_tool import CSVTool
from .excel_tool import ExcelTool
from .html_tool import HTMLTool
from .json_tool import JSONTool


class LoaderFactory:

    def __init__(self):

        self.csv = CSVTool()
        self.excel = ExcelTool()
        self.html = HTMLTool()
        self.json = JSONTool()

    def load(self, filepath):

        ext = Path(filepath).suffix.lower()

        if ext == ".csv":
            return self.csv.load(filepath)

        if ext in [".xls", ".xlsx"]:
            return self.excel.load(filepath)

        if ext in [".html", ".htm"]:
            return self.html.load(filepath)

        if ext == ".json":
            return self.json.load(filepath)

        raise ValueError(f"Unsupported file type: {ext}")
