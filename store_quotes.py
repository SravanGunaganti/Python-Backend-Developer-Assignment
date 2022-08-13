from asyncio.windows_events import NULL
import json 
import sqlite3

def get_json_data():
    with open('quotes.json','r') as read_file:
        obj_file = json.loads(read_file.read())
    return obj_file

def get_author_names_list(authors_list):
    authors_name_list = []
    for each_name in authors_list:
        if each_name['name'] not in authors_name_list:
            authors_name_list.append(each_name['name'].replace("-"," "))            
    return authors_name_list
         
def create_table(table,table_name):
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    drop_table = "DROP TABLE IF EXISTS {}"
    cursor.execute(drop_table.format(table_name))
    cursor.execute('''PRAGMA foreign_keys = ON''')
    cursor.execute(table)
    connection.commit()
    connection.close()

def retrieving_data_from_tables(query):
    connection = sqlite3.connect("quotes.db")
    cursor= connection.cursor()
    cursor.execute(query)
    query_solution= cursor.fetchone()
    connection.commit()
    connection.close()
    return query_solution

def insert_values_to_tables(query):
    connection  = sqlite3.connect('quotes.db')
    cursor= connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def insert_values_to_quotes_table(author_names_list,quote_obj):
    quote=quote_obj['quote'].replace('"',"'")
    author_name=quote_obj["author"]
    author_id=author_names_list.index(author_name)+1
    quote_query = '''INSERT INTO quotes(quote,author_id) VALUES("{}",{});'''
    formatted_quote_query=quote_query.format(quote,author_id)
    insert_values_to_tables(formatted_quote_query)

def insert_values_to_authors_table(author_obj):
    born =author_obj["born"]
    author_name=author_obj["name"]
    reference=author_obj["reference"]
    author_query='''
    INSERT INTO authors(author_name,born,reference) VALUES("{}","{}","{}");'''
    formatted_author_query=author_query.format(author_name,born,reference)
    insert_values_to_tables(formatted_author_query)
 
def insert_values_to_tags_table(tags_list,quote_id):
    for each_tag in tags_list:
        tags_query = '''INSERT INTO tags(tag_name,quote_id) VALUES("{}",{});'''
        formatted_tags_query = tags_query.format(each_tag,quote_id)
        insert_values_to_tables(formatted_tags_query)
        

def insert_author_quote_tags_details_to_tables(quotes_list,authors_list,author_names_list):
    for author_details in authors_list:
        insert_values_to_authors_table(author_details)
        
    quote_id=0
    for quote_details in quotes_list:
        quote_id+=1
        insert_values_to_quotes_table(author_names_list,quote_details)
        insert_values_to_tags_table(quote_details['tags'],quote_id)

def create_tables_queries():
    quotes_table='''
            CREATE TABLE quotes(
                id INTEGER NOT NULL PRIMARY KEY,
                quote VARCHAR,
                author_id INTEGER
                );
                '''
    authors_table='''
            CREATE TABLE authors(
                id INTEGER NOT NULL PRIMARY KEY,
                author_name VARCHAR(250),
                born VARCHAR(200),
                reference VARCHAR(250)
                );
                '''
    tags_table = '''
            CREATE TABLE tags(
                id INTEGER NOT NULL PRIMARY KEY,
                tag_name VARCHAR(250),
                quote_id INTEGER);
                '''
    
    
    create_table(quotes_table,"quotes")
    create_table(authors_table,"authors")
    create_table(tags_table,"tags")
    
    
def get_data_from_json():
    quotes_authors_json_data=get_json_data()
    quotes_list=quotes_authors_json_data["quotes"]
    authors_list=quotes_authors_json_data["authors"]
    author_names_list=get_author_names_list(authors_list)
    insert_author_quote_tags_details_to_tables(quotes_list,authors_list,author_names_list)

create_tables_queries()
get_data_from_json()