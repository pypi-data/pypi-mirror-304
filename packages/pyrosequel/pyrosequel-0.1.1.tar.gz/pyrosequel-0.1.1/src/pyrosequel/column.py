from .sqlfn import BinaryExpr, SQLBinaryOperator

class ColumnAttribute:
    pass
class PrimaryKey(ColumnAttribute):
    pass
class NotNull(ColumnAttribute):
    pass
class Cascade(ColumnAttribute):
    pass
class Default(ColumnAttribute):
    def __init__(self, default):
        self.default = default

class Field:
    def __init__(self, *attributes, field_name=None):
        self.attributes = attributes
        self.table_name = None
        self.field_name = field_name
    def __eq__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.EQ)
    def __ne__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.NEQ)
    def __gt__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.GT)
    def __ge__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.GTE)
    def __lt__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.LT)
    def __le__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.LTE)
    
    def __add__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.ADD)
    def __sub__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.SUB)
    def __mul__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.MUL)
    def __div__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.DIV)
    def __mod__(self, value):
        return BinaryExpr(self, value, SQLBinaryOperator.MOD)

class IntegerField(Field):
    pass
class TextField(Field):
    pass
class ForeignKeyField(Field):
    def __init__(self, foreign_column, on_delete=None, on_update=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_delete = on_delete
        self.on_update = on_update
        self.foreign_column = foreign_column

class Column:
    def __init__(self, sqltype, attributes):
        pass

class Everything:
    pass