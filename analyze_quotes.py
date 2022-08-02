import sqlite3


query_1 = '''
    SELECT 
        COUNT() as total_no_of_quotes
    FROM 
        quotes;
'''

query_2 = '''
    SELECT 
        author_name,
        COUNT() as total_no_of_quotes
    FROM 
        quotes
    WHERE 
        author_name = "Albert Einstein"
    GROUP BY 
        author_name;
'''

query_3 = '''
    SELECT
        MIN(no_of_tags) as min_no_of_tags,
        MAX(no_of_tags) as max_no_of_tags,
        AVG(no_of_tags) as avg_no_of_tags
        
    FROM 
        quotes;
'''

query_4 = '''
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
def retrieving_data_from_tables(query):
    connection = sqlite3.connect("quotes.db")
    cursor= connection.cursor()
    cursor.execute(query)
    query_solution= cursor.fetchall()
    connection.commit()
    connection.close()
    return query_solution

query1_solution=retrieving_data_from_tables(query_1)
query2_solution=retrieving_data_from_tables(query_2)
query3_solution=retrieving_data_from_tables(query_3)
query4_solution=retrieving_data_from_tables(query_4)

print(query1_solution)
print(query2_solution)
print(query3_solution)
print(query4_solution)
