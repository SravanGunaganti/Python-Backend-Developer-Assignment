import sqlite3

def start_connection_with_database():
    return sqlite3.connect("quotes.db")

def get_query_from_table(table_query):

    connection = start_connection_with_database()
    cursor_obj = connection.cursor()
    cursor_obj.execute(table_query)
    result = cursor_obj.fetchall()

    connection.commit()
    connection.close()
    print(result)

table_1 = '''
    SELECT 
        COUNT() as total_no_of_quotations
    FROM 
        quotes;
'''
table_2 = '''
    SELECT 
        author_name,
        COUNT() as total_no_of_quotations
    FROM 
        quotes
    WHERE 
        author_name = "Albert Einstein"
    GROUP BY 
        author_name;
'''
table_3 = '''
    SELECT
        MIN(no_of_tags) as minimum_no_of_tags,
        MAX(no_of_tags) as maximum_no_of_tags,
        AVG(no_of_tags) as average_no_of_tags
        
    FROM 
        quotes;
'''
table_4 = '''
    SELECT 
        author_id,
        author_name,
        COUNT() as no_of_quotes
    FROM 
        quotes
    GROUP BY 
        author_id
    ORDER BY 
        no_of_quotes DESC
    LIMIT 5
'''


get_query_from_table(table_1)
get_query_from_table(table_2)
get_query_from_table(table_3)
get_query_from_table(table_4)