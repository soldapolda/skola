# ACCESS LISTY (ACL)
- slouzi k omezeni provozu nebo pristupu do urcitych casti site
	- zvyseni bezpecnosti, omezeni pristupu k prostredkum ktere nepotrebuji
- filtrace dat na routeru
- standartni ACL jsou na treti vrste, rozsirene aji na ctvrte
- ACL se nastavuje na fyzicke porty routeru a muzou byt prichazi nebo odchozi
    - příchazí se vyhodnocuje první
    - o odchozích ??

## Příkazy

- ACL je seznam příkazů, kdy každý příkaz je buď:
    1. povolení - permit 
    2. zakázání - deny
- Když se najde shoda tak se příkaz provede a další už se nedělají
- Když se nenajde shoda tak se packet zahodí (jakoby DENY ALL)