class Book():
    book_text: str = "hOoMaN"
    likes: int = 4

    def __str__(self):
        return f'{self.book_text}, {self.likes}'


book = Book()
print(Book())