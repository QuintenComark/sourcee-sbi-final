from . import dbx
from sqlexecx.sql_exec import SqlExec as _SqlExec
from sqlexecx.page_exec import PageExec


class SqlExec(_SqlExec):

    def save(self, *args, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.exec.save(self.sql, *args, **kwargs)


def sql(sql: str) :
    assert sql, "Parameter 'sql' must not be none"
    return SqlExec(dbx, sql)


def page(page_num: int, page_size: int) :
    return PageExec(dbx, page_num, page_size)
