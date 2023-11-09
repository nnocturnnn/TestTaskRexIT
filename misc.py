import csv
import sys
import sqlite3
from typing import Iterator, Dict, List, Optional

def read_csv_iterator(file_path: str) -> Iterator[Dict[str, str]]:
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

def create_and_populate_database(data_iterator: Iterator[Dict[str, str]], database_path: str="users.db") -> None:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    create_table_query = f'CREATE TABLE IF NOT EXISTS users (category TEXT, firstname TEXT, lastname TEXT, email TEXT, gender TEXT, dob TEXT);'
    cursor.execute(create_table_query)
    for row in data_iterator:
        insert_query = f'INSERT INTO users (category, firstname, lastname, email, gender, dob) VALUES (:category, :firstname, :lastname, :email, :gender, :birthDate);'
        cursor.execute(insert_query, row)
    conn.commit()
    conn.close()


def get_filtered_data(per_page: int, page: int, filters: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    query = "SELECT * FROM users WHERE 1"
    params = []

    if filters:
        if 'category' in filters:
            query += " AND category = ?"
            params.append(filters['category'])
        if 'gender' in filters:
            query += " AND gender = ?"
            params.append(filters['gender'])
        if 'dob' in filters:
            query += " AND dob = ?"
            params.append(filters['dob'])
        if 'min_age' in filters and 'max_age' in filters:
            query += " AND strftime('%Y', 'now') - strftime('%Y', dob) BETWEEN ? AND ?"
            params.extend([filters['min_age'], filters['max_age']])
        elif 'min_age' in filters:
            query += " AND strftime('%Y', 'now') - strftime('%Y', dob) >= ?"
            params.append(filters['min_age'])
        elif 'max_age' in filters:
            query += " AND strftime('%Y', 'now') - strftime('%Y', dob) <= ?"
            params.append(filters['max_age'])

    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, (page - 1) * per_page])

    with sqlite3.connect("users.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
    return data


if __name__ == '__main__':
    data_iterator = read_csv_iterator(sys.argv[1])
    create_and_populate_database(data_iterator)
