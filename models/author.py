from database.connection import get_db_connection
from models.article import Article

class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self.name = name 

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:
            if not hasattr(self, "_name"):
                self._name = value
            else:
                raise AttributeError("Name cannot be changed after initialization.")
        else:
            raise ValueError("Name must be a non-empty string.")


    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["author_id"], article["magazine_id"], article["title"], article["id"]) for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category 
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id 
            WHERE articles.author_id = ?''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine["name"], magazine["category"], magazine["id"]) for magazine in magazines]

    def __repr__(self):
        return f"<Author {self.name}>"