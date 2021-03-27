import sqlite3
import os
def main():
    db_path = os.path.realpath("../DC4-data/firewall_data.db")
    conn = sqlite3.connect(db_path)
    print(conn.total_changes)

    cur = conn.cursor()
    # cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cur.fetchall())
    # t = ("Teardown", )
    # cur.execute("SELECT * FROM data \
    #     WHERE Operation=?", t)
    # print(cur.fetchone())
    # cur.execute("PRAGMA table_info(data);")
    # print(cur.fetchall())

    cur.execute("SELECT DISTINCT `Syslog Priority` \
         FROM data;")
    print(cur.fetchall())
    cur.execute("SELECT COUNT(*) FROM data \
        WHERE `Syslog Priority`=?", ('Critical',))
    print(cur.fetchone())
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()