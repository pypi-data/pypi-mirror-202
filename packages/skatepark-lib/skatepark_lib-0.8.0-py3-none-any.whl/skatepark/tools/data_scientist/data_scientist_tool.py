from attr import define, field
from skatepark.tools import Tool
from skatepark.utils import PythonRunner


@define
class DataScientistTool(Tool):
    libs: dict[str, str] = field(default={"math": "math"}, kw_only=True)

    def run(self, value: str) -> str:
        return PythonRunner(libs=self.libs).run(value)

    @property
    def schema_kwargs(self) -> dict:
        return {
            "imports": self.__imports()
        }

    def __imports(self):
        return str.join(", ", self.libs.values())
