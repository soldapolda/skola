# Formátování protokolů

## Stránka

- A4 na výšku, pokud konkrétní grafická příloha nevyžaduje stránku naležato.
- Běžné okraje: horní a dolní 12,5 mm, levý a pravý 25 mm.
- Titulní tabulka je širší než běžná textová oblast a musí zůstat vystředěná podle vzoru.
- Bez automaticky přidávaného záhlaví nebo zápatí.

## Písmo

- Běžný text protokolu: Times New Roman 12 pt.
- Hlavní nadpisy: Arial 12 pt, tučně, verzálkami.
- Rovnice: Cambria Math 11 pt prostřednictvím OMML, pokud konkrétní schválený vzor nestanoví jinak.
- Text v tabulkách: Times New Roman 12 pt, pokud šířka tabulky nevyžaduje individuální úpravu schválenou uživatelem.

## Odstavce

- Odborný text zarovnat do bloku.
- Zachovat střídmé mezery odpovídající vzorům.
- Nadpis nastavit jako „ponechat s následujícím“.
- Nerozdělovat krátké tabulky a rovnicové bloky nevhodně mezi stránky.
- Nepoužívat dekorativní barvy ani moderní design, které nejsou ve vzorech.

## Tabulky

- Skutečné tabulky Wordu s černým ohraničením.
- Nadpisy sloupců tučně.
- Jednotky uvádět přímo v záhlaví nebo u veličiny.
- Slučování buněk použít jen tehdy, když vyjadřuje logickou strukturu.
- Šířky sloupců nastavovat podle obsahu; tabulka nesmí přetékat mimo stránku.
- Přístrojová tabulka zachovává úzký první sloupec pro případné označení funkce přístroje.

## Titulní strana

- U protokolů s výpočtovými sekcemi kopírovat z `vzor_vypoctovych_sekci.docx`; u ostatních typů je obecným základem `protokol_1.docx`.
- Zachovat rozměry buněk, výšky řádků, okraje buněk a ohraničení.
- Vkládat jedno hlavní schéma a zkontrolovat jeho čitelnost v kontrolním PDF.
- Nepřidávat další obsah, který by změnil výšku stránky nebo posunul následující sekce.

## Závazný vzor výpočtových sekcí

Pro sekce obsažené ve `vzory/vzor_vypoctovych_sekci.docx` je tento dokument přímým sazebním vzorem ve všech budoucích protokolech, které příslušné sekce používají.

Referenční vzhled po vykreslení určuje `vzory/vzor_vypoctovych_sekci_word.pdf`, který vznikl převodem stejného DOCX v Microsoft Wordu 2016. Pomocný export z LibreOffice se může lišit kvůli substituci písem a odlišnému vykreslení OMML; nesmí být vydáván za přesnou Wordovou podobu.

- Zachovat A4 na výšku, okraje 12,5 mm nahoře a dole a 25 mm vlevo a vpravo.
- Zachovat návaznost `ZADÁNÍ` → `Zadané hodnoty` → `NÁHRADNÍ SCHÉMA` → ruční konec stránky → `VÝPOČTY` → `ZHODNOCENÍ`, pokud jsou všechny tyto sekce pro daný protokol relevantní.
- Zadané hodnoty sázet pomocí editovatelných vložených OMML výrazů v rozložení podle vzoru. Nepřevádět je automaticky na tabulku jen kvůli zarovnání.
- Náhradní schéma umístit a škálovat stejně jako ve vzoru; pro jiný obsah zachovat obdobnou šířku, čitelnost a odstupy.
- Výpočty členit krátkým textovým popisem a dvojicí rovnicových řádků. První řádek obsahuje obecný vztah a dosazení, druhý samostatný výsledek.
- Obecný vztah a dosazení sázet do jednoho `m:oMath` se zachovanou mezerou přesně podle archetypu předlohy. Výsledek patří do samostatného tučného OMML řádku pod pravou částí. Neviditelné dvousloupcové tabulky pro výpočty nepoužívat; reálný export z Microsoft Wordu 2016 prokázal, že rozbíjejí vodorovné i svislé rozestupy a mohou rozdělit jedinou rovnici. LibreOffice může mezery v OMML zobrazit sevřeně, ale rozhodující je vzhled ve Wordu podle `vzory/vzor_vypoctovych_sekci_word.pdf`.
- Krátký související výpočtový blok nerozdělit mezi stránky. Pokud se celý nevejde, přesunout jeho popis i rovnice na následující stránku.
- Na titulní straně zachovat také vertikální polohu schématu a řádků zadaných hodnot. Při odlišném poměru stran schématu použít pevné kompatibilní rozestupy a zarovnání hodnot do stabilních sloupců; kontrolní PDF nesmí mít nápadně prázdnou spodní část buňky.
- Rovnicové bloky jsou `m:oMathPara` se zarovnáním matematického obsahu vlevo. Vnější odstavec Wordu se nesmí použít k nahrazení vnitřního matematického zarovnání.
- Jednotky, mezery, desetinné čárky, indexy a pořadí zápisu přebírat přesně z odsouhlaseného obsahu a archetypu předlohy.
- Textové a značkové zvláštnosti vzoru se bez souhlasu uživatele neopravují. Přesná vizuální věrnost má v tomto případě přednost před normalizací.
