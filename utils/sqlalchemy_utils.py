# Models
class TableBase(object):

    def __repr__(self):
        return "<{class_name}({columns_and_values})>".format(
            class_name=self.__tablename__,
            columns_and_values=", ".join(
                [f"{col}={getattr(self, col.name)}" for col in self.__table__.columns]
            ),
        )

    @classmethod
    def drop(cls, checkfirst: bool = False, *args, **kwargs):
        if checkfirst:
            schema = cls.schema_name()
            table = cls.table_name()
            if cls.metadata.tables.get(f"{schema}.{table}") is None:
                print(f"`{schema}.{table}` table does not exist")
                return True
            else:
                print(f"Delete `{schema}.{table}` table")
                return cls.__table__.drop(checkfirst=checkfirst, *args, **kwargs)
        else:
            return cls.__table__.drop(*args, **kwargs)

    @classmethod
    def create(cls, checkfirst: bool = False, *args, **kwargs):
        return cls.__table__.create(checkfirst=checkfirst, *args, **kwargs)

    @classmethod
    def columns(cls):
        return [col.name for col in cls.__table__.columns]

    @classmethod
    def table_name(cls):
        assert cls.__tablename__ is not None
        return cls.__tablename__

    @classmethod
    def schema_name(cls):
        return "default" if cls.metadata.schema is None else cls.metadata.schema
