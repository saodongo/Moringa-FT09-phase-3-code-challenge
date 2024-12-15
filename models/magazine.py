from database.connection import get_db_connection
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id=None, name=None, category=""):
        self._id = id
        self.name = name
        self.category = category if category else "Uncategorized"  # Default value for category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = ?''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors]

    def article_titles(self):
        articles = self.articles()
        return [article.title for article in articles] if articles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name, COUNT(articles.id) as article_count
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id = ?
            GROUP BY authors.id 
            HAVING article_count > 2''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors] if authors else None

    def __repr__(self):
        return f"<Magazine {self.name} ({self.category})>"