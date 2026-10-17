# Schválená rozhodnutí

## 2026-10-17 – úloha ZELE 3Z

- Správným hlavním vzorem postupu je 24. příklad souboru `priklady_do_cviceni_2026_10_12_LMS.pdf`; lineární výpočet otáček při jiném zatížení se doplní podle 25. příkladu.
- Zadané hodnoty jsou `U_n = 400 V`, `f_n = 50 Hz`, `2p = 2`, `P_n = 7200 W`, `n_n = 2951 min⁻¹`, `I_n = 13 A`, `cos(φ_n) = 0,88`, `M_z/M_n = 2,1` a `I_z/I_n = 9`.
- Všechny zobrazené mezivýsledky se průběžně zaokrouhlují na tři desetinná místa. Závazné výsledky jsou `n_S = 3000,000 min⁻¹`, `n_X = 2975,500 min⁻¹`, `M_n = 23,299 N·m`, `I_z = 117,000 A`, `M_z = 48,928 N·m` a `η_n = 90,842 %`.
- Titulní strana obsahuje technické zobrazení třífázového asynchronního motoru. Původní orientační momentová charakteristika se vloží jako přesný výřez zdrojového PDF v těle protokolu a hodnoty se z ní neodečítají.
- Zapojení motoru do hvězdy nebo trojúhelníku se nebude tvrdit, protože je individuální zadání neurčuje.
- Momentová charakteristika je referenční náčrtek, nikoliv graf vytvořený ze zdrojových dat; XLSX se proto nevytváří.

## 2026-10-17 – úloha ZELE 4Z

- Zadané hodnoty jsou `U = 35 V`, `L₁ = 36 mH`, `R₁ = 32 Ω`, `L₂ = 41 mH`, `R₂ = 24 Ω` a `P = 2,1 W`.
- Řešení používá napěťový trojúhelník v pořadí `R → L → I → U_R → U_L → X_L → f → φ`.
- Každý zobrazený mezivýsledek se průběžně zaokrouhlí na tři desetinná místa a použije v následujícím kroku. Závazné výsledky jsou `I = 0,194 A`, `f = 354,481 Hz` a `φ = 71,917°`.
- Titulní strana obsahuje jedno hlavní schéma; v těle je samostatné náhradní schéma s prvky `R = R₁ + R₂` a `L = L₁ + L₂`.
- Po dokončení základního protokolu uživatel schválil jednu dodatečnou samostatnou stranu 4 s fázorovým diagramem a grafem `P(f)`. Původní strany 1–3 zůstávají beze změny a původní strana se zhodnocením se pouze přesouvá na stranu 5 bez vizuální změny.
- Graf `P(f)` má samostatný editovatelný soubor `graf_P_f.xlsx`. Rozlišuje přesný průsečík `355,194 Hz; 2,100 W` a výsledek protokolu s průběžným zaokrouhlováním `354,481 Hz; 2,108 W`.

## 2026-10-16 – zdroje semestrálního projektu ZELE a úloha 2Z

- Soubory `Zadání semestrálního projektu ZELE.pdf` a `ZELE_Parametry_zadání_SP_Út_17_45-19_15_2.pdf` jsou závazné zdroje zadání a individuálních hodnot pro příklady 1–5.
- Druhý příklad vznikne jako samostatný protokol ve složce `2Z-zele-2` a vizuálně naváže na ručně schválený protokol 1Z.
- Proud každého spotřebiče se určí ze vztahu `P = U·I·cos φ`, převede se do komplexního fázoru a celkový proud se získá součtem komplexních proudů. Samostatně označené osové složky `I_x` a `I_y` se nepoužijí. Spotřebiče 2 a 3 se podle motorových značek považují za induktivní.
- Protokol bude obsahovat přesný fázorový diagram proudů `I₁`, `I₂`, `I₃` a výslednice `I` se správnými úhly a jednotným měřítkem.
- Titulní údaje se převezmou z 1Z; název a číslo projektu se změní na `2Z` a téma na `Střídavý rozvod jištěný jističem`.
- Originální vypínací charakteristika bude anotována konstrukčními čarami a dostane samostatnou stránku. Výpočet `I/Iₙ = 3,153` patří pouze do sekce `VÝPOČTY`; na stránce charakteristiky se uvádí už jen „Velikost nadproudu: 3,153“ a minimální a maximální vypínací čas. Samotná charakteristika využije téměř celou dostupnou šířku stránky.
- Wordový export `protokol-4.pdf` zamítl variantu s neviditelnými dvousloupcovými tabulkami: vznikly nadměrné mezery, nechtěný třetí sloupec výsledků a zalomení komplexního výsledku. Výpočty 2Z se proto sázejí stejným způsobem jako ruční vzor: obecný vztah a dosazení v jediném OMML odstavci, výsledek na samostatném tučném řádku pod pravou částí. `protokol-2.pdf` potvrzuje tuto variantu jako blízkou cíli a `protokol-1.pdf` je rozhodující vizuální vzor.
- Titulní strana 2Z zachovává původní tabulku a vertikální rytmus vzoru 1Z; hlavní schéma je zvětšeno na dostupnou šířku a hodnoty jsou zarovnány ve čtyřech pevných sloupcích u spodní části buňky.
- Počet stran není omezen. Charakteristika se nebude zmenšovat na úkor čitelnosti.
- Vypínací charakteristika je referenční podklad, nikoliv graf vytvořený ze zdrojových dat; pro tuto úlohu se proto nevytváří XLSX.
- Poloha konstrukční svislice pro `I/Iₙ = 3,153` se kalibruje lokálně mezi skutečnými značkami 3 a 4 na logaritmické ose. Původní globální interpolace zobrazovala přibližně 3,3 a neoprávněně zasahovala do okamžité oblasti B. Opravený odečet je `tmin ≈ 6 s`, `tmax ≈ 21 s` v tepelné části pásma.

## 2026-10-17 – úloha ZELE 5Z

- Správným vzorem postupu je 14. příklad na tiskových stranách 7–8 souboru `priklady_do_cviceni_2026_10_12_LMS.pdf`.
- Zadané hodnoty jsou `U = 230 V`, `f = 50 Hz`, `P = 30 W`, `cos(φ) = 0,31` a `cos(φ′) = 0,95`.
- Všechny zobrazené mezivýsledky se průběžně zaokrouhlují na tři desetinná místa. Schválené výsledky jsou `C_K = 4,941 µF`, `I = 0,421 A` a `I′ = 0,137 A`.
- Praktická normalizovaná kapacita se nevybírá, protože ji zadání nepožaduje.
- Školní výpočet `√2·U = 325,269 V` se zachová, ale výsledek se označí jako amplituda napájecího napětí. AC jmenovité napětí kondenzátoru je samostatný údaj; součástka musí být určena pro trvalý provoz alespoň při `230 V AC / 50 Hz` a bezpečně snášet amplitudu i provozní přepětí.
- Fázorový diagram se geometricky konstruuje z nezaokrouhlených hodnot. Zobrazené popisky jsou zaokrouhleny na tři desetinná místa a kontrola se zapisuje komplexními proudy bez složek `I_x`, `I_y`.

## 2026-10-16 – ručně upravený protokol jako závazný vzor

- Ručně upravený soubor `1Z-zele-1/protokol.docx` byl přijat jako přesný zdroj vzhledu a uložen beze změny do `vzory/vzor_vypoctovych_sekci.docx`.
- Vzor je závazný ve všech projektech, které používají jeho titulní stranu nebo sekce `ZADÁNÍ`, `Zadané hodnoty`, `NÁHRADNÍ SCHÉMA`, `VÝPOČTY` či `ZHODNOCENÍ`. Jednotlivé sekce se stále zařazují jen tehdy, když je daný protokol potřebuje.
- Kopíruje se úplně přesně, včetně rozložení, mezer, ručního konce stránky, označení veličin, stylu rovnic a případných zdánlivých nekonzistencí nebo překlepů. Například `R_ST` v náhradním schématu a formulace „proudu na zátěží“ se bez výslovného pokynu uživatele nemění.
- Teoretický protokol nemá automaticky sekci `ÚVOD`. Výchozí pořadí podle tohoto vzoru je titulní strana, `ZADÁNÍ`, zadané hodnoty, případné `NÁHRADNÍ SCHÉMA`, `VÝPOČTY` a `ZHODNOCENÍ`.
- Výpočty používají nativní editovatelné OMML bloky, Cambria Math 11 pt, matematické zarovnání vlevo, obecný vztah a dosazení na jednom řádku a výsledek na samostatném řádku.
- Zjištěné charakteristiky referenčního souboru: 4 strany A4, jedna titulní tabulka, dva vložené obrázky, jeden ruční konec stránky, 50 objektů `m:oMath` a 26 bloků `m:oMathPara`.
- Toto rozhodnutí má přednost před staršími body, které jsou s ním v rozporu. Zejména nahrazuje dřívější strukturu prvního teoretického protokolu se sekcí `ÚVOD` a požadavek automaticky čistit nebo normalizovat prvky, které uživatel ve výsledném vzoru ponechal.
- Uživatel dodal PDF získané převodem tohoto DOCX v Microsoft Wordu 2016. Je uloženo jako `vzory/vzor_vypoctovych_sekci_word.pdf` a je závazným vizuálním referenčním náhledem.
- Dřívější rozdíl kontrolního PDF nebyl rozdílem DOCX: zdrojový a výstupní DOCX byly bajtově totožné. Rozdíl způsobil LibreOffice na Linuxu, který v aktuálním prostředí nahrazuje Times New Roman, Arial a Cambria Math fonty Liberation Serif, Liberation Sans a FreeSerif.
- `1Z-zele-1/vystup/kontrolni_nahled.pdf` nyní obsahuje uživatelem schválený Wordový náhled. Samostatný pomocný export z LibreOffice je uložen jako `kontrolni_nahled_libreoffice.pdf`.

## 2026-10-11

- Hlavní základ titulní strany: `vzory/protokol_1.docx`.
- Titulní strana vždy obsahuje právě jedno hlavní schéma.
- V dalších sekcích může být náhradní schéma potřebné pro výpočty.
- Vedle výsledného DOCX bude samostatný XLSX se zdrojovými daty a editovatelným grafem.
- Vizuální vzor grafu určuje `vzory/priklad_grafu.xlsx`.
- Podobu grafu ve Wordu určuje `vzory/jak_ma_graf_ve_wordu_vypadat.pdf`.
- Jeden graf dostane vlastní celou stránku.
- Dva grafy se mají přednostně vejít na jednu společnou stránku, pokud zůstanou čitelné.
- XLSX musí přehledně oddělit data, výpočty, mezivýpočty a graf.
- Chybné nebo poškozené rovnice z `protokol_2.docx` se nebudou přebírat.
- Osamoceným nadpisům na konci stránky se bude předcházet.
- Osobní údaje z titulní strany nejsou závazné; uživatel je může upravit.
- Cílem je kompatibilita s běžnými staršími verzemi Microsoft Wordu; pro vložená schémata se proto používá kompatibilní PNG a vektorový zdroj se uchovává samostatně.

## Ověřená písma

### Protokoly

- běžný text: Times New Roman 12 pt;
- hlavní nadpisy: Arial 12 pt tučně;
- rovnice: Cambria Math.

### PDF grafů

- název grafu: Arial Bold;
- hodnoty os: Aptos Regular;
- legenda a názvy os: převážně Aptos Bold;
- matematické části: Cambria Math;
- Times New Roman se v grafovém PDF nevyskytuje.

Kvůli kompatibilitě se staršími Office lze běžné grafové texty normalizovat na Arial; tato kompatibilní odchylka musí zachovat velikosti, rozvržení a celkový vzhled vzoru.

## První teoretický protokol – ZELE 1Z

- Protokol je čistě teoretický; neobsahuje přístroje, postup měření, naměřené hodnoty, graf ani XLSX.
- Původní plán struktury obsahoval `ÚVOD`; tento bod je nahrazen rozhodnutím z 2026-10-16 a závazná je ručně upravená čtyřstránková podoba.
- V celém protokolu se pro zátěž používá index `S`: `U_S`, `R_S`, `I_S`, `P_S`.
- Odpor zátěže `R_S = 33 mΩ` je přímý vstup. Obecný vztah `R = U_n²/P_n` se uvádí pouze informativně, protože jmenovitý výkon nebyl zadán.
- Ztráty se uvádějí po celých větvích A a B: `ΔP_A = I_A²R_A`, `ΔP_B = I_B²R_B`.
- Mezivýsledky se průběžně zaokrouhlují na tři desetinná místa a dále se používají zaokrouhlené hodnoty. Odpory vodičů se zaokrouhlují v mΩ; jejich převod do Ω zachovává všechny tři desetinné číslice hodnoty v mΩ.
- Dokument obsahuje právě jedno hlavní schéma na titulní straně a jedno náhradní schéma před výpočty; jejich konkrétní podoba je převzata z ručně schváleného vzoru beze změn.
