import enum

class SQLExpr:
    pass

class COUNT(SQLExpr):
    def __init__(self, item):
        self.item = item

class SQLBinaryOperator(enum.Enum):
    EQ = 1
    NEQ = 2
    GT = 3
    GTE = 4
    LT = 5
    LTE = 6

    AND = 10
    OR = 11

    ADD = 30
    SUB = 31
    DIV = 32
    MUL = 33
    MOD = 34

class BinaryExpr(SQLExpr):
    def __init__(self, val1, val2, op):
        self.val1 = val1
        self.val2 = val2
        self.op = op