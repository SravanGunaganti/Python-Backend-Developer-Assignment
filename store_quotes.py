import json 
import sqlite3

def get_json_data():
    with open('quotes.json','r') as read_file:
        obj_file = json.loads(read_file.read())
    return obj_file

quotes_table='''
        CREATE TABLE quotes(
            id INTEGER NOT NULL PRIMARY KEY,
            quote VARCHAR,
            author_name VARCHAR(250),
            no_of_tags INTEGER,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id) 
            ON DELETE CASCADE
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name VARCHAR(250),
            quote_id INTEGER,
            FOREIGN KEY (quote_id) REFERENCES quotes(id) 
            ON DELETE CASCADE
            );
            '''
def get_author_names_list(list_1):
    name_list = []
    for each_name in list_1:
        if each_name['author'] not in name_list:
            name_list.append(each_name['author'])            
    return name_list
   
quotes_authors_json_data=get_json_data()

quotes_list=quotes_authors_json_data["quotes"]
authors_list=quotes_authors_json_data["authors"]
author_names_list=get_author_names_list(quotes_list)

def create_table(table,table_name):
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    drop_table = "DROP TABLE IF EXISTS {}"
    cursor.execute(drop_table.format(table_name))
    cursor.execute('''PRAGMA foreign_keys = ON''')
    cursor.execute(table)
    connection.close()



create_table(quotes_table,"quotes")
create_table(authors_table,"authors")
create_table(tags_table,"tags")


def insert_values_to_tables(query):
    connection  = sqlite3.connect('quotes.db')
    cursor= connection.cursor()
    cursor.executescript(query)
    connection.commit()
    connection.close()

def insert_values_to_quotes_table(quote_table_id,quote_obj):
    quote=quote_obj['quote']   
    if quote_table_id ==91:
        quote= quote[:10]+quote[12:31]+quote[32:]
    author_name = quote_obj['author']
    no_of_tags = len(quote_obj['tags'])
    author_id = author_names_list.index(author_name)+1
    quote_query = '''
    INSERT INTO 
        quotes(id,quote,author_name,no_of_tags,author_id)
    VALUES(
        {},
       "{}",
       "{}",
        {},
        {}
    );
    '''
    formatted_quote_query=quote_query.format(quote_table_id,quote,author_name,no_of_tags,author_id)
    print(formatted_quote_query)
    insert_values_to_tables(formatted_quote_query)

#Insert_values_authors_table
def insert_values_to_authors_table(author_obj,author_table_id):
    born =author_obj["born"]
    author_name=author_obj["name"]
    reference=author_obj["reference"]
    author_query='''
    INSERT INTO 
        authors(id,author_name,born,reference)
    VALUES(
         {},
        "{}",
        "{}",
        "{}"
    );
'''
    formatted_author_query=author_query.format(author_table_id,author_name,born,reference)
    insert_values_to_tables(formatted_author_query)

#Insert_tags_table    
def insert_tags_to_tags_table(quote_count,tags_list):
    for each_tag in tags_list:
        tags_query = '''
    INSERT INTO 
        tags(tag_name,quote_id)
    VALUES(
    "{}",
     {}
    );
    '''     
        formatted_tags_query = tags_query.format(each_tag,quote_count)
        insert_values_to_tables(formatted_tags_query)

author_table_id=1
for author_dictionary in authors_list:
    insert_values_to_authors_table(author_dictionary,author_table_id)
    author_table_id+=1

quote_table_id=1
for quote_dictionary in quotes_list:
    insert_values_to_quotes_table(quote_table_id,quote_dictionary)
    insert_tags_to_tags_table(quote_table_id,quote_dictionary['tags'])
    quote_table_id+=1