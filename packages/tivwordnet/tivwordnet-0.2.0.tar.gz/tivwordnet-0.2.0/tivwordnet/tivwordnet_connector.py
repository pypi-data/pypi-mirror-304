import sqlite3
import os

class TivWordnetConnector:
    
    DIRECTORY = 'tiv_database'
    DB_NAME = 'tivwordnet.db'

    def __init__(self, directory=None):
        if not directory:
            directory = self.DIRECTORY
        filename = os.path.join(directory, self.DB_NAME)
        # Mhen u or a dirigi mba u taver
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.db_path = os.path.join(os.path.dirname(__file__), filename)
        
        # Yan u mba or taver taver ior u we na ga ior
        print(f"Database file path: {self.db_path}")
        
        try:
            # U gban u taver
            self.db = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cur = self.db.cursor()
            self._create_tables()  # Mhen u aondo u mu u mban
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
    
    def __enter__(self):
        """Mhen u gban u taver se mba u  aondo u  kpa.""" 
        try:
            self.db = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cur = self.db.cursor()
            self._create_tables()
            return self
        except sqlite3.Error as e:
            print(f"Error entering context for database connection: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        """Mhen u mu taver se mba u  aondo u  ka taver.""" 
        if self.db:
            try:
                self.db.commit()
                self.db.close()
                print("Database connection closed successfully.")
            except sqlite3.Error as e:
                print(f"Error while closing the database connection: {e}")

    def _create_tables(self):
        """Mhen u mu u aondo u mban se mba u  kpa.""" 
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS synsets(
                                synset_id INTEGER NOT NULL,
                                lemma TEXT NOT NULL,
                                definition TEXT NOT NULL,
                                UNIQUE(synset_id, lemma, definition)
                                );''')
            self.cur.execute('''CREATE TABLE IF NOT EXISTS hypernyms(
                                sid INTEGER NOT NULL,
                                hypersid INTEGER NOT NULL,
                                UNIQUE(sid, hypersid)
                                );''')
            self.db.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def insert_synsets(self, synsets):
        """Mhen u or u aondo u synsets mba u  kpa.""" 
        print(f"Inserting synsets: {synsets}")
        query = '''INSERT INTO synsets(synset_id, lemma, definition) VALUES (?, ?, ?)'''
        try:
            self.cur.executemany(query, synsets)
            self.db.commit()
            print(f"Successfully inserted {len(synsets)} synsets.")
        except sqlite3.Error as e:
            print(f"Error inserting synsets: {e}")

    def insert_hypernyms(self, hypernyms):
        """Mhen u or u aondo u hypernyms mba u  kpa.""" 
        print(f"Inserting hypernyms: {hypernyms}")
        query = '''INSERT INTO hypernyms(sid, hypersid) VALUES (?, ?)'''
        try:
            self.cur.executemany(query, hypernyms)
            self.db.commit()
            print(f"Successfully inserted {len(hypernyms)} hypernyms.")
        except sqlite3.Error as e:
            print(f"Error inserting hypernyms: {e}")

    def get_synsets(self):
        """Mhen u aondo u synsets u synsets table.""" 
        try:
            self.cur.execute('SELECT * FROM synsets')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving synsets: {e}")
            return []

    def get_hypernyms(self):
        """Mhen u aondo u hypernyms u hypernyms table.""" 
        try:
            self.cur.execute('SELECT * FROM hypernyms')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving hypernyms: {e}")
            return []

    def display_all_data(self):
        """Mhen u kpishi or aondo u synsets ken hypernyms mba u  aondo u kpa.""" 
        synsets = self.get_synsets()
        hypernyms = self.get_hypernyms()
        print("Synsets in the database:")
        for synset in synsets:
            print(synset)
        print("Hypernyms in the database:")
        for hypernym in hypernyms:
            print(hypernym)
