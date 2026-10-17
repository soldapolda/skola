# Elektrotechnické protokoly – trvalá pravidla projektu

## Účel projektu

Tento projekt slouží k individuální tvorbě odborných protokolů z elektrotechnických měření. Nejde o pevný formulářový generátor. AI vždy nejprve vyhodnotí konkrétní zadání, naměřené hodnoty, fotografie výpočtů, schémata a další podklady a teprve podle nich navrhne obsah dokumentu.

Primární pracovní prostředí je Linux. Cílovým prostředím výsledného DOCX je Microsoft Word na Windows, včetně běžných starších instalací přibližně generace Office 2016. Kontrola v LibreOffice je pouze předběžná; nikdy netvrdit, že byl dokument ověřen v Microsoft Wordu, pokud se tak skutečně nestalo.

Komunikace s uživatelem probíhá česky a používá správnou elektrotechnickou terminologii.

## Závazné zdroje a jejich ochrana

Referenční soubory ve `vzory/` jsou neměnné originály:

- `protokol_1.docx` – aplikace IO NE555; hlavní základ titulní strany;
- `protokol_2.docx` – generátor funkcí; zdroj složitější struktury výpočtů, nikoli bezchybný matematický vzor;
- `protokol_3.docx` – LabVIEW; zdroj struktury tabulky naměřených hodnot;
- `vzor_vypoctovych_sekci.docx` – ručně upravený závazný vzor titulní strany a sekcí `ZADÁNÍ`, `Zadané hodnoty`, `NÁHRADNÍ SCHÉMA`, `VÝPOČTY` a `ZHODNOCENÍ`;
- `vzor_vypoctovych_sekci_word.pdf` – závazný vizuální náhled stejného dokumentu převedeného uživatelem z Microsoft Wordu 2016;
- `priklad_grafu.xlsx` – závazný vizuální vzor excelových grafů;
- `jak_ma_graf_ve_wordu_vypadat.pdf` – závazný vzor výsledné podoby grafu ve Wordu.

Zdrojové zadání semestrálního projektu v kořeni projektu je rovněž neměnné:

- `Zadání semestrálního projektu ZELE.pdf` – společné pokyny, texty příkladů, schémata a pomocné charakteristiky pro úlohy 1–5;
- `ZELE_Parametry_zadání_SP_Út_17_45-19_15_2.pdf` – individuální parametry Vojtěcha Solanského pro úlohy 1–5.

Při zpracování dalších úloh ZELE se vždy použije text příslušného příkladu z prvního PDF a číselné hodnoty stejného příkladu z druhého PDF. Oba zdroje se kopírují do podkladů konkrétní úlohy, ale originály v kořeni projektu se neupravují.

Referenční soubory nikdy nepřepisovat ani neupravovat. Pro práci vždy vytvořit kopii v adresáři konkrétního měření.

`vzor_vypoctovych_sekci.docx` má pro uvedené typy sekcí přednost před staršími obecnými doporučeními a před vzhledem rovnic v `protokol_1.docx` až `protokol_3.docx`. Pravidlo se uplatňuje ve všech protokolech, ve kterých se daná sekce objeví; neznamená to, že každý protokol musí obsahovat všechny tyto sekce. Vzhled, rozložení, způsob zápisu rovnic, zalomení a textové konvence se kopírují přesně. Bez výslovného pokynu uživatele se neopravují ani zdánlivé nekonzistence, překlepy nebo odlišná označení ve vzoru.

Pro cílový vzhled má přednost `vzor_vypoctovych_sekci_word.pdf`. LibreOffice na tomto Linuxu nemá původní Windows fonty Times New Roman, Arial a Cambria Math a nahrazuje je jinými fonty, takže jeho PDF může vypadat jinak i při bajtově totožném DOCX. LibreOffice náhled je pomocná kontrola přetečení a integrity, nikoli důkaz pixelové shody s Microsoft Wordem.

Podrobná pravidla jsou v:

- `pravidla/analyza_vzoru.md`;
- `pravidla/struktura.md`;
- `pravidla/formatovani.md`;
- `pravidla/grafy.md`;
- `pravidla/workflow.md`;
- `pravidla/rozhodnuti.md`.

## Povinný schvalovací postup

Při novém měření:

1. Prostudovat všechny dodané podklady.
2. Sepsat dostupné a chybějící informace.
3. Neodhadovat chybějící odborné ani naměřené údaje.
4. Navrhnout strukturu celého protokolu a položit pouze otázky, které ovlivňují správnost nebo podobu výsledku.
5. Připravit jeden kompletní textový návrh všech sekcí.
6. Počkat na společné schválení celého návrhu.
7. Teprve po schválení vytvořit DOCX, XLSX a grafické podklady.
8. Provést obsahovou, matematickou, strukturální a vizuální kontrolu.

Uživatel nechce schvalovat každou sekci samostatně.

## Teoretické projekty bez měření

- U čistě teoretického projektu se nevytvářejí prázdné sekce `POUŽITÉ PŘÍSTROJE`, `POSTUP MĚŘENÍ`, tabulka naměřených hodnot ani graf.
- Výchozí jádro podle ručně upraveného vzoru je `ZADÁNÍ`, blok zadaných hodnot, případně `NÁHRADNÍ SCHÉMA`, `VÝPOČTY` a `ZHODNOCENÍ`.
- Sekce `ÚVOD` se nepřidává automaticky; použije se jen tehdy, když ji vyžaduje zadání nebo ji uživatel schválí.
- Zhodnocení musí výslovně rozlišit teoretický model od experimentálně ověřeného výsledku.
- Jestliže protokol neobsahuje graf, nevytváří se prázdný XLSX pouze kvůli obecnému pravidlu pro grafické protokoly.

## Titulní strana

- Pro protokol s výpočtovými sekcemi podle ručně upraveného vzoru je základem kopie titulní strany z `vzor_vypoctovych_sekci.docx`. Pro jiné typy protokolu zůstává obecným základem `protokol_1.docx`.
- Zachovat původní osm řádkovou tabulku, sloučení buněk, rozměry, okraje a ohraničení.
- Titulní tabulku znovu nestavět, pokud to není technicky nezbytné.
- Na titulní straně bude vždy právě jedno hlavní elektrické schéma.
- Další náhradní schéma může být v následujících sekcích, zejména pokud slouží k odvození nebo výpočtům.
- Osobní údaje z výchozí šablony nejsou závazným profilem; uživatel je může upravit.

## Text, tabulky a sazba

- Běžný text: Times New Roman 12 pt.
- Hlavní nadpisy protokolu: Arial 12 pt, tučně, verzálkami, vlevo.
- Běžné odstavce převážně zarovnat do bloku.
- Nadpis svázat s následujícím odstavcem, tabulkou nebo rovnicí, aby nezůstal sám na konci stránky.
- Počet stran není pevný.
- Tabulky vytvářet jako skutečné tabulky Wordu, nikoli jako obrázky.
- Přístrojová tabulka má čtyři sloupce; první úzký sloupec je volitelný pro funkční označení přístroje.
- Barevné zvýraznění z `protokol_3.docx` není univerzální pravidlo.

## Rovnice a matematická kontrola

- Samostatné výpočty vytvářet jako nativní editovatelné rovnice Wordu ve formátu OMML a s matematickým písmem Cambria Math.
- V sekci `VÝPOČTY` kopírovat archetypy rovnic z `vzor_vypoctovych_sekci.docx`: blokové `m:oMathPara`, matematické zarovnání vlevo, Cambria Math 11 pt, obecný vztah vlevo, číselné dosazení v pevném pravém sloupci a výsledná hodnota pod dosazením.
- Výpočtové bloky podle ruční předlohy sázet jako jediný nativní OMML odstavec: obecný vztah vlevo, zachovaná mezera a dosazení vpravo; tučný výsledek je v samostatném OMML odstavci pod pravou částí. Nepoužívat pro tento účel neviditelné tabulky – v Microsoft Wordu 2016 vedly k nadměrným rozestupům, nechtěnému třetímu sloupci a zalamování rovnic.
- Existující funkční OMML bloky z předlohy klonovat a měnit jejich obsah; rovnice bez důvodu znovu nesestavovat jiným mechanismem.
- LaTeX lze použít pouze jako meziformát.
- Zachovat původní označení veličin, indexy, exponenty, řecká písmena, jednotky a pořadí obecný vztah → dosazení → výsledek.
- Přepis originálu a matematická kontrola jsou dvě samostatné činnosti.
- Při zjištění chyby uvést původní zápis, konkrétní problém a správný výsledek; neopravovat obsah bez souhlasu uživatele.
- Nečitelné symboly nehádat.
- Chybné nebo poškozené rovnice z `protokol_2.docx` se nesmějí převzít jako vzor.
- Numerické výpočty ověřit vhodným nástrojem a kontrolovat převody jednotek, znaménka, zaokrouhlení a relativní chyby.
- Pokud uživatel schválí průběžné zaokrouhlování, každý zobrazený mezivýsledek se použije v následujícím kroku. Malé odpory se mohou zaokrouhlovat v mΩ a následně převést do Ω bez další ztráty číslic; například `75,433 mΩ = 0,075433 Ω`.
- Vznikne-li kvůli průběžnému zaokrouhlování malý rozdíl v kontrolní proudové nebo výkonové bilanci, uvést jeho velikost a příčinu.

## Schémata

- Schéma musí být technicky správné; estetika nesmí převážit nad správností zapojení.
- Kontrolovat propojení, polarity, svorky, hodnoty součástek, směry proudů a označení napětí.
- Zdrojový vektorový soubor uchovat samostatně, pokud vznikne.
- Pro širokou kompatibilitu se starším Wordem vkládat do DOCX kvalitní PNG; SVG uchovat vedle dokumentu jako zdroj.
- Náhradní a fázorová schémata mohou být umístěna mimo titulní stranu podle obsahu měření.

## Grafy a XLSX

- Každý graf musí mít samostatný editovatelný zdrojový soubor XLSX vedle výsledného DOCX.
- XLSX musí obsahovat vstupní data, jednotky, vzorce, mezivýpočty, výsledné řady a skutečný editovatelný graf.
- Pro číselné osy používat bodový graf XY, pokud charakter měření nevyžaduje jiný typ.
- Vizuální styl vychází z `priklad_grafu.xlsx`; přesná pravidla jsou v `pravidla/grafy.md`.
- Graf má ve Wordu vlastní celou stránku. Pokud jsou grafy dva, přednostně je umístit společně na jednu stránku a zachovat čitelnost.
- Graf vytvořit rovnou v cílovém poměru a velikosti; nečitelnost neřešit pouhým zmenšením hotového grafu.
- Do Wordu vložit kvalitní kompatibilní náhled vytvořený z XLSX. Editovatelnost musí vždy zůstat v samostatném XLSX.

## Kontrola výstupu

Před odevzdáním:

- ověřit všechny sekce, hodnoty, jednotky, tabulky, rovnice, grafy a schémata;
- ověřit integritu balíčků DOCX a XLSX;
- vykreslit DOCX přes LibreOffice do PDF a obrázků stran;
- je-li k dispozici Wordový referenční PDF, porovnat cílový vzhled primárně s ním a LibreOffice náhled označit jako pomocný;
- vizuálně prohlédnout každou stránku;
- zkontrolovat přetečení textu, oříznuté rovnice, osamocené nadpisy, rozbité tabulky, posunuté objekty a čitelnost grafů;
- po opravě kontrolu zopakovat;
- zachovat samostatné XLSX a zdrojové soubory schémat.

## Organizace měření

Každé nové měření má vlastní složku pod `mereni/`. Doporučená struktura je popsána v `pravidla/struktura.md`. Pracovní a odvozené soubory nikdy neukládat do `vzory/`.
