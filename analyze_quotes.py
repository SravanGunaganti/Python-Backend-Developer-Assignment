import sqlite3

def retrieving_data_from_tables(query):
    connection = sqlite3.connect("quotes.db")
    cursor= connection.cursor()
    cursor.execute(query)
    query_solution= cursor.fetchall()
    connection.commit()
    connection.close()
    return query_solution

def querying_data_from_database():
    no_of_quotes_query = '''SELECT COUNT() as total_no_of_quotes 
                            FROM quotes;'''
    
    no_of_quotes_by_author_query = '''
        SELECT COUNT()
        FROM quotes INNER JOIN authors ON authors.id=quotes.author_id
        WHERE author_name = "Albert Einstein";'''
    
    min_max_avg_no_of_tags_query= '''SELECT MIN(no_of_tags),MAX(no_of_tags),AVG(no_of_tags) FROM quotes;'''

    top_authors_with_no_of_quotes_query= '''
        SELECT author_name,count(quote) as no_of_quotes
        FROM quotes INNER JOIN authors ON quotes.author_id=authors.id
        GROUP BY author_id 
        ORDER BY no_of_quotes DESC ,author_id ASC
        LIMIT 5
        ;'''
    
    no_of_quotes=retrieving_data_from_tables(no_of_quotes_query)
    print("Total no.of quotations on the website: ",no_of_quotes[0][0])
    
    no_of_quotes_by_author=retrieving_data_from_tables(no_of_quotes_by_author_query)
    print("No of quotations authored by Albert Einstein: ",no_of_quotes_by_author[0][0])
    
    min_max_avg_no_of_tags=retrieving_data_from_tables(min_max_avg_no_of_tags_query)
    print("Min of tags:"+str(min_max_avg_no_of_tags[0][0])," Max of tags:"+str(min_max_avg_no_of_tags[0][1])," Avg of tags:"+str(int(min_max_avg_no_of_tags[0][2])))
    
    top_authors_with_no_of_quotes=retrieving_data_from_tables(top_authors_with_no_of_quotes_query)
    top_authors_list=[ '''{}:{} '''.format(author_item[0],author_item[1]) for author_item in top_authors_with_no_of_quotes]
    print(*top_authors_list)
querying_data_from_database()