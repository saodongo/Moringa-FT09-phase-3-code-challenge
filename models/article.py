from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        if not id:
            self._create_article()

    def _create_article(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) 
            VALUES (?, ?, ?, ?)''', (self.title, self.content, self.author_id, self.magazine_id))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise ValueError("id must be an integer")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 50:
            if not hasattr(self, "_title"):
                self._title = value
            else:
                raise AttributeError("Title cannot be changed after initialization.")
        else:
            raise ValueError("Title must be a string between 5 and 50 characters.")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise ValueError("Content must be a string.")

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if isinstance(value, int):
            self._author_id = value
        else:
            raise ValueError("Author ID must be an integer.")

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if isinstance(value, int):
            self._magazine_id = value
        else:
            raise ValueError("Magazine ID must be an integer.")

    def __repr__(self):
        return f"<Article {self.title} by Author ID {self.author_id} in Magazine ID {self.magazine_id}>"