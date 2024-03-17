import sqlite3

# Connect to SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('prompt.db')
cursor = conn.cursor()

# Create Generations table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Generations (
        generation_id INTEGER PRIMARY KEY,
        model_id INTEGER,
        seed_id INTEGER,
        prompt_id INTEGER,
        output TEXT,
        FOREIGN KEY (model_id) REFERENCES Models(model_id),
        FOREIGN KEY (seed_id) REFERENCES Seeds(seed_id),
        FOREIGN KEY (prompt_id) REFERENCES Prompts(prompt_id)
    )
''')

# Create Models table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Models (
        model_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# Create Seeds table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Seeds (
        seed_id INTEGER PRIMARY KEY,
        value INTEGER
    )
''')

# Create Prompts table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prompts (
        prompt_id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        prompt TEXT,
        pgroup_id INTEGER,
        obsolete INTEGER,
        FOREIGN KEY (pgroup_id) REFERENCES Pgroups(pgroup_id)
    )
''')

# Create Pgroups table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pgroups (
        pgroup_id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()
