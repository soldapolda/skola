# Uvod do OSPF (Open Shortest Path First)

- protokol typu stav linky, bere stav linky a hlavně její propustnost
- není proprietalní žádné firmy -> je free

## Funkce

1. routry posílají "Hello packety" svým sousedům, pomocí nich se dohodnou na parametrech a vytvoří stav "sousedství"
2. sousední routery si vzájemně vyměňují aktualizační packety - LSU
    - obsahují LSA neboli informace o stavu linky
3. všechny routery si ukládají přijaté LSA do topologické databáze
    - topologickou databázi mají všechny routery stejnou
4. po naplnění databáze každý router provede výpočet optimální cesty pomocí "Djikstova algoritmu"
    - pro tento výpočet je potřeba výkonný hardware
    - výsledkem je nalezení optimální cesty
5. na základě vypočtených dat si router vyplní routovací tabulku