from sqlalchemy.types import UserDefinedType

# -----------------------------
# Custom Vector Type for TiDB
# -----------------------------
class Vector(UserDefinedType):
    def __init__(self, dimensions: int):
        self.dimensions = dimensions

    def get_col_spec(self, **kw):
        return f"VECTOR({self.dimensions})"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            # ✅ Convert list of floats → string "[0.1, 0.2, ...]"
            return "[" + ",".join(str(float(x)) for x in value) + "]"
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            # TiDB usually returns a string like "[0.1,0.2,...]"
            if isinstance(value, str):
                return list(map(float, value.strip("[]").split(",")))
            return value
        return process