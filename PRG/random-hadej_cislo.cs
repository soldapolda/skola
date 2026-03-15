Random random = new Random();
int pocet_pokusu = 12;

Console.WriteLine($"Myslim si cislo pd 1 do 100 a mas {pocet_pokusu} pokusu");
int cislo_k_uhodnuti = random.Next(1, 101);

int pocet_hadani = 0;
bool uhodnuto = false;

while (pocet_hadani < pocet_pokusu) {

    Console.Write($"\nZadej cislo ({pocet_hadani + 1}/{pocet_pokusu}): ");
    string input = Console.ReadLine();

    int cislo;
    if (!int.TryParse(input, out cislo))
    {
        Console.WriteLine("ZADEJ POUZE PLATNY FORMAT CELEHO CISLA");
        continue;
    }

    if (cislo < 1 || cislo > 100)
    {
        Console.WriteLine("ZADEJ CISLO V INTERVALU 1 AZ 100");
        continue;
    }

    if (cislo > cislo_k_uhodnuti)
    {
        Console.WriteLine("Nizsi");
    }

    if (cislo < cislo_k_uhodnuti)
    {
        Console.WriteLine("Vyssi");
    }

    if (cislo == cislo_k_uhodnuti)
    {
        uhodnuto = true;
        break;
    }

    pocet_hadani++;
}

if (uhodnuto)
{
    Console.WriteLine("\nVYHRAL!!!!!");
} else
{
    Console.WriteLine($"\nPROHRAL...");
    Console.WriteLine($"Hadane cislo bylo - {cislo_k_uhodnuti}");
}
