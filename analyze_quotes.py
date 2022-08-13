import sqlite3

def retrieving_data_from_tables(query):
    connection = sqlite3.connect("quotes.db")
    cursor= connection.cursor()
    cursor.execute(query)
    query_solution= cursor.fetchall()
    connection.commit()
    connection.close()
    return query_solution

def querying_data_from_database(no_of_quotes,no_of_quotes_by_author,min_max_avg_of_tags,top5_authors):
    no_of_quotes_result=retrieving_data_from_tables(no_of_quotes)
    print("Total no.of quotations on the website: ",no_of_quotes_result[0][0])
    
    no_of_quotes_by_author_result=retrieving_data_from_tables(no_of_quotes_by_author)
    print("No of quotations authored by Albert Einstein: ",no_of_quotes_by_author_result[0][0])
    
    min_max_avg_of_tags_result=retrieving_data_from_tables(min_max_avg_of_tags)
    print("Min no.of tags:"+str(min_max_avg_of_tags_result[0][0]))
    print("Max no.of tags:"+str(min_max_avg_of_tags_result[0][1]))
    print("Avg no.of tags:"+str(int(min_max_avg_of_tags_result[0][2])))
    
    top5_authors_result= retrieving_data_from_tables(top5_authors)
    top5_authors_list=[]
    for item in top5_authors_result:
        top5_authors_list.append(item[0]+": "+str(item[1]))
    print("Top5_authors : ",*top5_authors_list)

def initializing_queries():
    no_of_quotes = '''SELECT COUNT() as total_no_of_quotes FROM quotes;'''
    
    no_of_quotes_by_author= '''
                            SELECT COUNT()
                            FROM quotes INNER JOIN authors ON authors.id=quotes.author_id
                            WHERE author_name = "Albert Einstein";
                            '''
    
    min_max_avg_of_tags= '''
                        SELECT MIN(no_of_tags),MAX(no_of_tags),AVG(no_of_tags) 
                        FROM(SELECT quotes.id,count(tags.id) as no_of_tags
                        FROM quotes LEFT JOIN tags ON tags.quote_id=quotes.id
                        GROUP BY quotes.id);
                        '''
    
    top_authors= '''
                SELECT author_name,count(quote) as no_of_quotes
                FROM quotes INNER JOIN authors ON quotes.author_id=authors.id
                GROUP BY author_id 
                ORDER BY no_of_quotes DESC ,author_id ASC
                LIMIT 5;
                '''
        
    querying_data_from_database(no_of_quotes,no_of_quotes_by_author,min_max_avg_of_tags,top_authors)
        
initializing_queries()