import sqlite3


create_tables_script = '''
CREATE TABLE query (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  created_at DATETIME,
  string VARCHAR(9999),
  url_template VARCHAR(9999),
  url VARCHAR(9999),
  search_engine_name VARCHAR(9999)
);

CREATE TABLE search_engine (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name VARCHAR(9999),
  url VARCHAR(9999),
  rank INTEGER
);
'''


if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.executescript(create_tables_script)
    conn.close()
