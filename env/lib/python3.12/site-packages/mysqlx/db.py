from . import sql_support
# Don't remove. Import for not repetitive implementation
from sqlexecx import insert, save, batch_insert, batch_execute, do_execute, do_save_sql, do_get, do_query,\
    do_query_one, do_select,do_select_one, do_select_page, do_query_page, do_select_page, do_query_page, load, do_load, insert_from_csv,\
    insert_from_df, insert_from_json, truncate_table, drop_table, table


def execute(sql: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO user(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('MySQLX.db.execute', sql, *args, **kwargs)
    return do_execute(sql, *args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('MySQLX.db.get', sql, *args, **kwargs)
    return do_get(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('MySQLX.db.query', sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('MySQLX.db.query_one', sql, *args, **kwargs)
    return do_query_one(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('MySQLX.db.select', sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_dynamic_sql('MySQLX.db.select_one', sql, *args, **kwargs)
    return do_select_one(sql, *args)


# ----------------------------------------------------------Page function------------------------------------------------------------------
def query_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_page_mapping('query_page', sql, page_num, page_size, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def select_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = sql_support.try_page_mapping('select_page', sql, page_num, page_size, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


from .sql_page_exec import sql, page
