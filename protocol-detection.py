import subprocess
import sys
import sqlite3
import glob
import re
import os
import time
from multiprocessing.pool import ThreadPool
from concurrent import futures

DB_NAME = "sites.db"
DS_FILE = "top1m.csv"
LAST_INDEX_FILE = "last_index"
THREADPOOL_CAP = 20

class Entry:
    id = 0
    domain = None
    server_name = None
    headers_frame = None
    max_frame_size = None
    max_header_list_size = None
    header_table_size = None
    max_concurrent_streams = None
    initial_window_size = None
    def __init__(self):
        super().__init__()
    def to_tuple(self):
        return (self.id, 
        self.domain, 
        self.server_name, 
        self.headers_frame,
        self.max_frame_size,
        self.max_header_list_size,
        self.header_table_size, 
        self.max_concurrent_streams, 
        self.initial_window_size)

def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS websites (
        id integer PRIMARY KEY,
        domain text NOT NULL,
        server_name text,
        headers_frame int,
        max_frame_size int,
        max_header_list_size int,
        header_table_size int,
        max_concurrent_streams int,
        initial_window_size int
    );
    ''')
    c.execute('create UNIQUE index domain on websites(domain);')
    conn.close()

def process(curl = 0):
    idx = 0
    try:
        last_idx_f = open(LAST_INDEX_FILE, 'r')
        idx = int(last_idx_f.readline())
        last_idx_f.close()
    except:
        pass
    try:
        f = open(DS_FILE, 'r')
    except:
        print("Cannot find dataset file top1m.csv")
        return
    
    print("Started at line {}".format(idx))

    start_time = time.time()

    count = 0
    entries = []
    args_list = []

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for _ in range(idx):
        next(f)
    for line in f:
        count += 1

        t = tuple(line.split(","))
        _id, domain = int(t[0]), str(t[1]).strip()
        args_list.append((_id, domain))

        if count % THREADPOOL_CAP == 0:
            elapsed_time = time.time() - start_time
            print("Current index " + str(idx))
            print("Sites visited: {}, elapsed: {:.2f}(s), requests/s: {:.2f}".format(count, elapsed_time, (count / elapsed_time)))

            p = ThreadPool(THREADPOOL_CAP)
            pool_output = p.starmap(requestNghttp, args_list)
            p.close()
            p.join()
            entries = [entry.to_tuple() for entry in pool_output]
            c.executemany('INSERT OR IGNORE INTO websites(id, domain, server_name, headers_frame, max_frame_size, max_header_list_size, header_table_size, max_concurrent_streams, initial_window_size) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', entries)
            print("Update " + str(c.rowcount))
            conn.commit()
            
            args_list = []
            idx += THREADPOOL_CAP
            f_l = open(LAST_INDEX_FILE, "w")
            f_l.seek(0)
            f_l.write(str(idx))
            f_l.truncate()
            f_l.close()

def requestNghttp(id, domain):
    entry = Entry()
    entry.id = id
    entry.domain = domain
    entry.headers_frame = -1
    # -n: Hide payload
    # -v: Verbose
    # -t: Time out 3 s
    result = subprocess.run(['nghttp', '-nvt', '5', 'https://' + domain], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try: 
        string_result = str(result.stdout.decode('utf-8'))
    except:
        print("Error decoding string result")
        return entry
    
    if "[ERROR]" in string_result:
        return entry

    entry.headers_frame = 1 if "recv HEADERS" in string_result else 0

    match = re.search("SETTINGS_MAX_CONCURRENT_STREAMS.*:.*\]", string_result)
    if match is not None:
        entry.max_concurrent_streams = int(match.group(0)[:-1].split(":")[-1])

    match = re.search("SETTINGS_INITIAL_WINDOW_SIZE.*:.*\]", string_result)
    if match is not None:
        entry.initial_window_size = int(match.group(0)[:-1].split(":")[-1])
    
    match = re.search("SETTINGS_MAX_FRAME_SIZE.*:.*\]", string_result)
    if match is not None:
        entry.max_frame_size = int(match.group(0)[:-1].split(":")[-1])

    match = re.search("SETTINGS_HEADER_TABLE_SIZE.*:.*\]", string_result)
    if match is not None:
        entry.header_table_size = int(match.group(0)[:-1].split(":")[-1])

    match = re.search("SETTINGS_MAX_HEADER_LIST_SIZE.*:.*\]", string_result)
    if match is not None:
        entry.max_header_list_size = int(match.group(0)[:-1].split(":")[-1])

    server_name = re.search("[Ss]erver:.*[^\r\n]", string_result)
    if server_name is not None:
        entry.server_name = str(server_name.group(0)).split(":")[-1].strip()
    
    return entry

def fix():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM websites WHERE headers_frame = -1 AND id >= 10000 AND id <= 13000 ORDER BY id DESC LIMIT 1000")
    rows = c.fetchall()
    begin = time.time()
    count = 0
    p = futures.ThreadPoolExecutor(20)
    begin = time.time()
    for r in rows:
        f = p.submit(requestNghttp, r[0], r[1])
        result = f.result().to_tuple()
        
        if result[3] != -1:
            print(result)
            query = '''
            UPDATE websites SET 
            headers_frame = ?, 
            max_frame_size = ?, 
            max_header_list_size = ?, 
            header_table_size = ?, 
            max_concurrent_streams = ?, 
            initial_window_size = ?
            WHERE id = ?
            '''
            c.execute(query, result[3:] + (r[0],))
            conn.commit()

if __name__ == "__main__":
    if os.path.exists(DB_NAME) == False:
        create_db()
    if "fix" in sys.argv:
        fix()
    else:
        process()

    