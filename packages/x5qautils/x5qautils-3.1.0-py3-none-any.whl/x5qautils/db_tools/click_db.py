import allure


@allure.step('Send request to db')
def request_db(db_client, sql_query):
    return db_client.execute(sql_query)


@allure.step('Format sql query to clickhouse db')
def get_custom_ch_query(query_string, *args):
    with allure.step('Create query'):
        query_group = query_string.format(*args)
        allure.attach(str(query_group), name='query', attachment_type=allure.attachment_type.TEXT)
        return query_group
