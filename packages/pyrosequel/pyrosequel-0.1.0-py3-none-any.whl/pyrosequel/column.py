from .sqlfn import CompareExpr

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
        return CompareExpr(self, value)
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