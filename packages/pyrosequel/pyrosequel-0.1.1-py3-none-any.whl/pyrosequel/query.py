from .column import Everything

class Query:
    def __init__(self, model):
        self.model = model
        self.clauses = []
    async def cast(self):
        raise NotImplementedError("Abstract Query cannot be casted")
    async def cast_and_fetch_one(self):
        raise NotImplementedError("Abstract Query cannot be casted")
    
    def where(self, expr):
        assert not any([isinstance(i, WhereClause) for i in self.clauses]), "WHERE clause can only appear once"
        self.clauses.append(WhereClause(expr))
        return self
    
    def left_join(self, table, expr):
        self.clauses.append(LeftJoinClause(table, expr))
        return self
    def inner_join(self, table, expr):
        self.clauses.append(InnerJoinClause(table, expr))
        return self
    
    def returning(self, *columns):
        assert not any([isinstance(i, ReturningClause) for i in self.clauses]), "RETURNING clause can only appear once"
        self.clauses.append(ReturningClause(columns))
        return self

class Clause:
    pass

class ReturningClause(Clause):
    def __init__(self, columns):
        self.columns = columns
class WhereClause(Clause):
    def __init__(self, expr):
        self.expr = expr
class HavingClause(Clause):
    def __init__(self, expr):
        self.expr = expr
class GroupByClause(Clause):
    def __init__(self, expr):
        self.expr = expr

class LeftJoinClause(Clause):
    def __init__(self, on, expr):
        self.on = on
        self.expr = expr
class InnerJoinClause(Clause):
    def __init__(self, on, expr):
        self.on = on
        self.expr = expr

class UnionClause(Clause):
    def __init__(self, other):
        self.other = other

class SelectQuery(Query):
    def __init__(self, model, selected):
        super().__init__(model)
        self.selected = selected
    
    async def cast(self):
        return await self.model.__database__.cast_select(self)
    
    def union(self, other):
        self.clauses.append(UnionClause(other))
        return self

class InsertQuery(Query):
    def __init__(self, model, inserting):
        super().__init__(model)

        self.model = model
        self.inserting = inserting

        self.select_query = None
    
    async def cast(self):
        return await (await self.model.__database__.cast_insert(self)).fetchone()
    
    async def select(self, select_query):
        assert self.select_query is None, "Only one SELECT query can be used in INSERT; use UNION instead"
        self.select_query = select_query
        return self