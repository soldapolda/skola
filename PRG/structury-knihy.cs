// Ukol 1

//Console.Write("Tvoje jmeno: ");
//string name = Console.ReadLine();

//using (StreamWriter writer = new StreamWriter("D:\\Users\\SolanskýVojtěch\\Desktop\\uzivatele.txt"))
//{ 
//    writer.WriteLine(name);
//}

//using (StreamReader reader = new StreamReader("D:\\Users\\SolanskýVojtěch\\Desktop\\uzivatele.txt"))
//{
//    Console.WriteLine($"Tvoje jmeno je: {reader.ReadLine()}");
//}


// Ukol 2

public class Program
{
    public struct Book
    {
        public string Title;
        public string Author;
        public int Year;
        public bool IsBorrowed;

        public Book(string title, string author, int year, bool isBorrowed)
        {
            this.Title = title;
            this.Author = author;
            this.Year = year;
            this.IsBorrowed = isBorrowed;
        }

        public void PrintInfo()
        {
            string borrowedText = this.IsBorrowed ? "Pujcena" : "Volna";
            Console.WriteLine($"{this.Title} {this.Author} ({this.Year}) - {borrowedText}");
        }

        public void Borrow()
        {
            this.IsBorrowed = true;
        }

        public void Return()
        {
            this.IsBorrowed = false;
        }
    }

    static LinkedList<Book> books = new LinkedList<Book>(new[]
    {
        new Book("1984", "George Orwell", 1949, true),
        new Book("To Kill a Mockingbird", "Harper Lee", 1960, false),
        new Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, false),
        new Book("Pride and Prejudice", "Jane Austen", 1813, true),
        new Book("The Catcher in the Rye", "J.D. Salinger", 1951, false)
    });

    static void PrintAllBooks()
    {
        foreach (Book book in books)
        {
            book.PrintInfo();
        }
    }

    static Book? FindOneBook(string title)
    {
        return books.FirstOrDefault(book => book.Title == title);
    }
    static void Main()
    {
        Program.PrintAllBooks();

        string bookTitle = "Pride and Prejudice";
        Book? findedBook = Program.FindOneBook(bookTitle);

        if (findedBook == null)
        {
            Console.WriteLine($"book {bookTitle} not found");
        }
        else
        {
            Console.Write("\nKniha keru hledas: ");
            findedBook.Value.PrintInfo();
        }
    }
}
