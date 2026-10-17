# Analýza referenčních vzorů

Datum analýzy: 2026-10-11

## Přehled

| Soubor | Skutečný obsah | Počet stran v LibreOffice | Rovnice OMML | Obrázky |
|---|---|---:|---:|---:|
| `protokol_1.docx` | Aplikace IO NE555 | 3 | 15 | 2 PNG |
| `protokol_2.docx` | Generátor funkcí | 4 | 36 | 3 PNG |
| `protokol_3.docx` | LabVIEW – analýza signálů | 4 | 9 | 1 PNG |

Původní slovní popis zaměňoval `protokol_1.docx` a `protokol_3.docx`. Vždy se řídit skutečným obsahem souborů.

## Společné technické vlastnosti

- Formát stránky: A4 na výšku, interně přibližně 209,9 × 296,6 mm.
- Horní a dolní okraj: přibližně 12,5 mm.
- Levý a pravý okraj běžného textu: přibližně 25 mm.
- Bez obsahu záhlaví a zápatí.
- Výchozí dokumentové písmo: Times New Roman.
- Běžný text: převážně Times New Roman 12 pt.
- Hlavní nadpisy: Arial 12 pt, tučně, verzálkami.
- Matematické písmo: Cambria Math.
- Dokumenty pocházejí z Microsoft Wordu 16 a šablony `Normal.dotm`.

## Titulní tabulka

Všechny tři dokumenty používají tutéž osm řádkovou titulní tabulku:

- celková šířka přibližně 184,3 mm;
- pět základních sloupců přibližně 60,4; 14,0; 52,1; 1,4 a 56,4 mm;
- vnější čáry přibližně 1 pt;
- vnitřní čáry přibližně 0,5 pt;
- pole schémat má pevnou výšku přibližně 166,8 mm;
- spodní pole poznámek, známky a data přibližně 29,8 mm.

Titulní stránka není oddělena běžným ručním zalomením. Přechod na další stranu vzniká výškou tabulky a tokem dokumentu. Proto se musí vždy provést kontrolní vykreslení.

## Společné sekce

1. ÚKOL MĚŘENÍ
2. POUŽITÉ PŘÍSTROJE
3. POSTUP MĚŘENÍ
4. PŘÍKLAD VÝPOČTU
5. ZHODNOCENÍ

Podmíněné prvky zahrnují tabulky hodnot, další schémata, grafy, dílčí odvození a přílohy.

## Zjištěné nedostatky vzorů

### Protokol 2

- Některé rovnice integrátoru obsahují viditelně poškozené znaky.
- Relativní chyba amplitudy vychází 2,00 %, ale jedna rovnice uvádí 3,6 %.
- Relativní chyba kmitočtu vychází přibližně 0,25 %, zatímco jeden odstavec uvádí 0,15 %.
- Tyto chyby se nesmějí přenášet do nových protokolů.

### Protokol 3

- Nadpis `ZHODNOCENÍ:` zůstal osamocený na konci třetí strany.
- Nové dokumenty musí používat vazbu nadpisu s následujícím obsahem.

## Obrázky a grafy

Schémata jsou vložena jako plovoucí PNG ukotvené v buňce titulní tabulky. Jejich umístění je křehké, proto je vhodné zachovat původní titulní konstrukci.

Žádný ze tří DOCX neobsahuje graf ani vložený Excel. Standard grafů proto určují samostatné soubory `priklad_grafu.xlsx` a `jak_ma_graf_ve_wordu_vypadat.pdf`.

## Rozsah vizuálního ověření

Všechny dokumenty byly vykresleny a prohlédnuty v LibreOffice na Linuxu. Vzhled v Microsoft Wordu nebyl v rámci této analýzy přímo ověřen.

## Doplňující závazný vzor po ruční úpravě

Datum doplnění: 2026-10-16

Uživatelem ručně upravený `1Z-zele-1/protokol.docx` je uložen jako `vzory/vzor_vypoctovych_sekci.docx`. Nejde pouze o obsahový příklad, ale o přímý vizuální a strukturální vzor pro každou z jeho sekcí, pokud se daná sekce použije v budoucím protokolu.

### Ověřená struktura

- čtyři strany A4 na výšku;
- okraje 709 twip nahoře a dole, 1418 twip vlevo a vpravo;
- jedna osm řádková titulní tabulka;
- dvě vložená PNG schémata;
- jeden ruční konec stránky před sekcí `VÝPOČTY`;
- 50 objektů `m:oMath` a 26 bloků `m:oMathPara`;
- hlavní schéma 555 × 285 px vložené v rozsahu 5 946 775 × 3 053 715 EMU;
- náhradní schéma 535 × 313 px vložené v rozsahu 5 204 924 × 3 045 124 EMU.

### Sazební sled stran

1. Titulní tabulka, hlavní schéma a blok vstupních hodnot pod schématem.
2. `ZADÁNÍ`, `Zadané hodnoty`, `NÁHRADNÍ SCHÉMA` a náhradní schéma.
3. `VÝPOČTY`: odpory vodičů a větví, uzlová rovnice, napětí a proudy, začátek výpočtu výkonu.
4. Dokončení výkonu, ztráty, účinnost a `ZHODNOCENÍ`.

Samostatný `ÚVOD` ve vzoru není. Výpočtové mezititulky jsou běžným textem. Bloková rovnice používá vlevo zarovnaný matematický obsah: obecný vztah a dosazení jsou na jednom řádku, výsledek je na samostatném řádku. Rovnice jsou editovatelné OMML s písmem Cambria Math 11 pt.

Při použití vzoru se zachovávají i prvky, které by se při běžné redakci mohly považovat za nekonzistentní. Ty lze opravit jen po výslovném pokynu uživatele. Přepis vzoru a odborná nebo matematická kontrola proto zůstávají dvěma oddělenými činnostmi.

### Kontrola přesné kopie

Výstup `1Z-zele-1/vystup/protokol.docx` byl porovnán se vzorem. Kontrola potvrdila shodný SHA-256, shodnou strukturu DOCX a pixelovou shodu všech čtyř stran po nezávislém vykreslení obou souborů v LibreOffice 7.3.7.2. Toto neznamená přímé ověření v Microsoft Wordu.

Uživatel následně dodal `vzory/vzor_vypoctovych_sekci_word.pdf`, vytvořený převodem stejného DOCX v Microsoft Wordu 2016. Tento soubor je rozhodujícím vizuálním referenčním náhledem. Jeho odlišnost od LibreOffice PDF je způsobena vykreslovacím prostředím, nikoli rozdílem mezi zdrojovým a výstupním DOCX. Na použitém Linuxu se požadované fonty nahrazují: Times New Roman → Liberation Serif, Arial → Liberation Sans a Cambria Math → FreeSerif.
