from dotenv import load_dotenv
import os

import duckdb

def main():
    load_dotenv()

    conn = duckdb.connect('md:sample_data')
    print(conn.sql("SHOW DATABASES").show())

    print(conn.sql("SELECT * FROM sample_data.nyc.taxi LIMIT 5;"))


if __name__ == "__main__":
    main()
