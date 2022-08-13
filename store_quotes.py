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

def get_tags_list(quotes_list):
    tags_list=[]
    for each in quotes_list:
        for tag in each["tags"]:
            if tag not in tags_list:
                tags_list.append(tag)
    return tags_list
            
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
    no_of_tags = len(quote_obj['tags'])
    author_name=quote_obj["author"]
    author_id=author_names_list.index(author_name)+1
    quote_query = '''INSERT INTO quotes(quote,author_id,no_of_tags) VALUES("{}",{},{});'''
    formatted_quote_query=quote_query.format(quote,author_id,no_of_tags)
    insert_values_to_tables(formatted_quote_query)

def insert_values_to_authors_table(author_obj):
    born =author_obj["born"]
    author_name=author_obj["name"]
    reference=author_obj["reference"]
    author_query='''
    INSERT INTO authors(author_name,born,reference) VALUES("{}","{}","{}");'''
    formatted_author_query=author_query.format(author_name,born,reference)
    insert_values_to_tables(formatted_author_query)
 
def insert_values_to_tags_table(tags_list): 
    for each_tag in tags_list:
        tag_query='''SELECT * FROM tags WHERE tag_name="{}";'''.format(each_tag)
        if retrieving_data_from_tables(tag_query)==None:
            tags_query = '''INSERT INTO tags(tag_name) VALUES("{}");'''
            formatted_tags_query = tags_query.format(each_tag)
            insert_values_to_tables(formatted_tags_query)
        
def insert_values_to_quotes_tags_table(quote_id,tags_list,quote_obj):
    tags=quote_obj["tags"]
    for tag in tags:
        tag_id=tags_list.index(tag)+1
        quotes_tags_query='''INSERT INTO quotes_tags(quote_id,tag_id) VALUES({},{});'''
        formatted_quotes_tags_query = quotes_tags_query.format(quote_id,tag_id)
        insert_values_to_tables(formatted_quotes_tags_query)
    
        

def insert_author_quote_tags_details_to_tables(quotes_list,authors_list,author_names_list,tags_list):
    for author_details in authors_list:
        insert_values_to_authors_table(author_details)
        
    quote_id=0
    for quote_details in quotes_list:
        quote_id+=1
        insert_values_to_quotes_table(author_names_list,quote_details)
        insert_values_to_tags_table(quote_details['tags'])
        insert_values_to_quotes_tags_table(quote_id,tags_list,quote_details)

def create_tables_queries():
    quotes_table='''
            CREATE TABLE quotes(
                id INTEGER NOT NULL PRIMARY KEY,
                quote VARCHAR,
                author_id INTEGER,
                no_of_tags INTEGER
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
                tag_name VARCHAR(250));
                '''
    
    quotes_tags_table='''
            CREATE TABLE quotes_tags(
                id INTEGER NOT NULL PRIMARY KEY,
                quote_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (quote_id) REFERENCES quotes(id) 
                ON DELETE CASCADE
                FOREIGN KEY (tag_id) REFERENCES tags(id) 
                ON DELETE CASCADE
                
                );
                '''
    create_table(quotes_table,"quotes")
    create_table(authors_table,"authors")
    create_table(tags_table,"tags")
    create_table(quotes_tags_table,"quotes_tags")
    
    
def get_data_from_json():
    quotes_authors_json_data=get_json_data()
    quotes_list=quotes_authors_json_data["quotes"]
    authors_list=quotes_authors_json_data["authors"]
    author_names_list=get_author_names_list(authors_list)
    tags_list=get_tags_list(quotes_list)
    insert_author_quote_tags_details_to_tables(quotes_list,authors_list,author_names_list,tags_list)

create_tables_queries()
get_data_from_json()