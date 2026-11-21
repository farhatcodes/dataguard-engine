from dataclasses import asdict, dataclass
from typing import Any

@dataclass(frozen=True)
class Violation:
    row: int
    field: str
    rule: str
    message: str

    def to_dict(self):
        return asdict(self)

def validate(records: list[dict[str, Any]], schema: dict[str, dict]) -> list[Violation]:
    violations = []
    for index, record in enumerate(records):
        for field, rules in schema.items():
            value = record.get(field)
            if rules.get("required") and (value is None or value == ""):
                violations.append(Violation(index, field, "required", "Value is required"))
                continue
            if value is None:
                continue
            kind = rules.get("type")
            types = {"string": str, "integer": int, "number": (int, float), "boolean": bool}
            if kind is not None:
                if kind not in types:
                    raise ValueError(f"Unsupported type: {kind}")
                valid = isinstance(value, types[kind])
                if kind in {"integer", "number"} and isinstance(value, bool):
                    valid = False
                if not valid:
                    violations.append(Violation(index, field, "type", f"Expected {kind}"))
                    continue
            if "min" in rules and value < rules["min"]:
                violations.append(Violation(index, field, "min", f"Must be >= {rules['min']}"))
            if "max" in rules and value > rules["max"]:
                violations.append(Violation(index, field, "max", f"Must be <= {rules['max']}"))
    return violations
