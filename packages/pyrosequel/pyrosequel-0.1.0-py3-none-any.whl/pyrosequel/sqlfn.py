class SQLExpr:
    pass

class COUNT(SQLExpr):
    def __init__(self, item):
        self.item = item

class CompareExpr(SQLExpr):
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2