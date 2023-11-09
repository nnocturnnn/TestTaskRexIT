import csv
import sys
import sqlite3
from typing import Iterator, Dict

def read_csv_iterator(file_path: str) -> Iterator[Dict[str, str]]:
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

def create_and_populate_database(data_iterator: Iterator[Dict[str, str]], database_path: str="users.db") -> None:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    create_table_query = f'CREATE TABLE IF NOT EXISTS users (category TEXT, firstname TEXT, lastname TEXT, email TEXT, gender TEXT, birthDate TEXT);'
    cursor.execute(create_table_query)
    for row in data_iterator:
        insert_query = f'INSERT INTO users (category, firstname, lastname, email, gender, birthDate) VALUES (:category, :firstname, :lastname, :email, :gender, :birthDate);'
        cursor.execute(insert_query, row)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    data_iterator = read_csv_iterator(sys.argv[1])
    create_and_populate_database(data_iterator)
