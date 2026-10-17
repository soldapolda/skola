# Grafy a sešity XLSX

## Závazné vzory

- `vzory/priklad_grafu.xlsx` určuje vizuální styl a chování editovatelného grafu.
- `vzory/jak_ma_graf_ve_wordu_vypadat.pdf` určuje výslednou podobu grafu na stránce Wordu.

Vzorový XLSX není závazným vzorem organizace tabulkových dat. Nové sešity musí být přehlednější.

## Ověřená typografie vzoru

Písma byla ověřena extrakcí vložených TrueType fontů z PDF:

- název grafu: Arial Bold;
- hodnoty os: Aptos Regular;
- legenda a běžné názvy os: převážně Aptos Bold;
- matematické znaky a anotace: Cambria Math;
- Times New Roman se v PDF grafů nevyskytuje.

XLSX používá motivové písmo Aptos/Aptos Narrow. Protože cílem jsou i starší instalace Wordu a Excelu, které Aptos nemusí mít, je povolena kompatibilní normalizace běžných textů grafu na Arial. Matematické anotace zůstávají Cambria Math. Název grafu vždy Arial Bold. Pokud je jisté, že cílové prostředí Aptos podporuje, lze ponechat Aptos přesně podle vzoru.

## Vizuální pravidla

- Typ: bodový graf XY s vyhlazenými spojnicemi, pokud fyzikální charakter dat nevyžaduje jiný typ.
- Pozadí: bílé, bez dekorativních efektů.
- Název: verzálky, Arial Bold, referenčně 14 pt.
- Hodnoty os: referenčně 8 pt.
- Názvy os: tučně, referenčně 10 až 10,5 pt.
- Legenda: dole, referenčně 9 pt.
- Skutečná hodnota: tmavě zelená spojnice přibližně 1,5 pt, značka `+` velikosti 7.
- Požadovaná hodnota: hnědo-oranžová spojnice přibližně 1,25 pt, značka `+` velikosti 5.
- Hlavní mřížka: tmavší zelená, přibližně 0,75 pt.
- Vedlejší mřížka: světlejší zelená, přibližně 0,75 pt.
- Technické anotace: Cambria Math, referenčně 8 pt, vhodné indexy a měřicí šipky.

Rozsahy os, hlavní a vedlejší kroky se stanovují podle skutečných dat. Číselné rozsahy z referenčního grafu nejsou univerzální.

Při vložení do Wordu se graf vytvoří rovnou v cílové velikosti. Velikosti písem se upraví tak, aby po vložení odpovídaly referenci a zůstaly čitelné; hotový velký graf se nesmí pouze výrazně zmenšit.

## Umístění ve Wordu

- Jeden graf: vlastní celá stránka a maximální rozumná plocha stránky.
- Dva grafy: přednostně společně na jedné stránce, obvykle pod sebou; musí zůstat čitelné názvy, osy a legenda.
- Pokud dva grafy na jedné stránce čitelné nejsou, použijí se dvě stránky.
- Výsledný DOCX obsahuje kompatibilní kvalitní náhled; editovatelný zdroj je samostatný XLSX ve stejné výstupní složce.

## Struktura nového XLSX

Preferovaná struktura:

### List `Data`

- pouze původní vstupní nebo naměřené hodnoty;
- jeden řádek na jeden záznam;
- jasné názvy veličin a jednotky;
- žádné skryté nahrazování dat ručně zadanými výsledky.

### List `Výpočty`

- pojmenované mezivýpočty;
- excelové vzorce odkazující na `Data`;
- jednotky, zaokrouhlení a vysvětlení významu;
- jasně rozlišit vstupy, mezivýpočty a konečné výsledky.

### List `Graf`

- finální datové řady použité grafem;
- případné pomocné řady s popisem účelu;
- samotný editovatelný graf;
- nastavená tisková oblast, pokud se má list tisknout nebo exportovat.

Vzor obsahuje chybný výraz `NED` namísto `NA()` a nestejné rozsahy některých řad. Tyto chyby se nepřebírají.

## Kontrola

- Ověřit, že změna vstupní hodnoty aktualizuje výpočty i graf.
- Ověřit rozsahy všech datových řad.
- Ověřit názvy a jednotky os.
- Ověřit legendu, barvy, značky a mřížku.
- Otevřít nebo vykreslit XLSX v LibreOffice jako předběžnou kompatibilní kontrolu.
- Po vložení do DOCX zkontrolovat výslednou velikost textů na stránce.
