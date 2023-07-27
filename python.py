class Book:
    def __init__(self, title, author, genre, is_available=True):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_available = is_available

class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.load_data()  # Load existing data from the file (if any)

    def add_book(self, book):
        self.books.append(book)
        self.save_data()

    def add_user(self, user):
        self.users.append(user)
        self.save_data()

    def display_available_books(self):
        available_books = [book for book in self.books if book.is_available]
        if available_books:
            print("Available Books:")
            for i, book in enumerate(available_books, 1):
                print(f"{i}. {book.title} by {book.author} ({book.genre})")
        else:
            print("No books available in the library.")

    def borrow_book(self, book, user):
        if book in self.books and book.is_available:
            user.borrowed_books.append(book)
            book.is_available = False
            self.save_data()
            return True
        return False

    def return_book(self, book, user):
        if book in user.borrowed_books:
            user.borrowed_books.remove(book)
            book.is_available = True
            self.save_data()
            return True
        return False

    def save_data(self):
        data = {
            "books": [
                {"title": book.title, "author": book.author, "genre": book.genre, "is_available": book.is_available}
                for book in self.books
            ],
            "users": [
                {"name": user.name, "email": user.email, "borrowed_books": [book.title for book in user.borrowed_books]}
                for user in self.users
            ],
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)

            for book_data in data["books"]:
                book = Book(book_data["title"], book_data["author"], book_data["genre"], book_data["is_available"])
                self.books.append(book)

            for user_data in data["users"]:
                user = User(user_data["name"], user_data["email"])
                for title in user_data["borrowed_books"]:
                    book = next((b for b in self.books if b.title == title), None)
                    if book:
                        user.borrowed_books.append(book)
                self.users.append(user)

        except FileNotFoundError:
            # If the file doesn't exist, start with an empty library
            pass


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.borrowed_books = []


def main():
    library = Library()

    while True:
        print("\n===== Digital Library Menu =====")
        print("1. Display Available Books")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. Add a New Book")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            library.display_available_books()

        elif choice == "2":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            user = User(name, email)

            library.display_available_books()
            book_num = int(input("Enter the book number you want to borrow: ")) - 1

            if 0 <= book_num < len(library.books):
                book = library.books[book_num]
                if library.borrow_book(book, user):
                    print(f"Successfully borrowed {book.title}!")
                else:
                    print("Sorry, the book is not available for borrowing.")
            else:
                print("Invalid book number.")

        elif choice == "3":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            user = next((u for u in library.users if u.name == name and u.email == email), None)

            if user:
                if user.borrowed_books:
                    print("Borrowed Books:")
                    for i, book in enumerate(user.borrowed_books, 1):
                        print(f"{i}. {book.title} by {book.author} ({book.genre})")

                    book_num = int(input("Enter the book number you want to return: ")) - 1
                    if 0 <= book_num < len(user.borrowed_books):
                        book = user.borrowed_books[book_num]
                        if library.return_book(book, user):
                            print(f"Successfully returned {book.title}!")
                        else:
                            print("You did not borrow this book.")
                    else:
                        print("Invalid book number.")
                else:
                    print("You have not borrowed any books.")
            else:
                print("User not found.")

        elif choice == "4":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            genre = input("Enter the genre of the book: ")

            book = Book(title, author, genre)
            library.add_book(book)

            print(f"Successfully added {title} by {author} ({genre}) to the library.")

        elif choice == "5":
            print("Exiting the Digital Library.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
