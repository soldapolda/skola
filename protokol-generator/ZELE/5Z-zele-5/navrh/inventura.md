# Inventura podkladů – ZELE 5Z

## Závazné zdroje

- `podklady/Zadání semestrálního projektu ZELE.pdf`
  - text 5. příkladu;
  - schéma skutečného zapojení;
  - náhradní schéma;
  - vzor fázorového diagramu a jeho měřítka.
- `podklady/ZELE_Parametry_zadání_SP_Út_17_45-19_15_2.pdf`
  - individuální hodnoty Vojtěcha Solanského pro 5. příklad.
- `podklady/priklady_do_cviceni_2026_10_12_LMS.pdf`
  - 14. příklad jako závazný vzor postupu výpočtu.
- `../vzory/vzor_vypoctovych_sekci.docx`
  - závazný zdroj titulní strany, sazby textu a OMML rovnic.
- `../vzory/vzor_vypoctovych_sekci_word.pdf`
  - rozhodující vizuální reference pro Microsoft Word 2016.

## Ověřené zadané hodnoty

- napájecí napětí `U = 230 V`;
- frekvence `f = 50 Hz`;
- činný příkon svítidla `P = 30 W`;
- původní účiník `cos(φ) = 0,31`;
- požadovaný účiník po kompenzaci `cos(φ′) = 0,95`.

## Požadované výsledky

- kapacita kompenzačního kondenzátoru `C_K`;
- minimální jmenovité napětí kondenzátoru `U_nC`;
- proud svítidla bez kompenzace `I`;
- proud svítidla po kompenzaci `I′`;
- fázorový diagram napětí a proudů před kompenzací a po ní.

## Schválená rozhodnutí

- Jde o teoretickou úlohu bez měření; nebudou sekce `POUŽITÉ PŘÍSTROJE`, `POSTUP MĚŘENÍ`, tabulka naměřených hodnot ani XLSX.
- Všechny zobrazené mezivýsledky se zaokrouhlí na tři desetinná místa a dále se použijí v této podobě.
- Uvede se pouze teoreticky vypočtená kapacita. Praktická normalizovaná hodnota kondenzátoru se nebude vybírat, protože ji zadání nepožaduje.
- Napěťové dimenzování zachová školní výpočet amplitudy `U_m = √2·U = 325,269 V`, ale nebude tuto amplitudu zaměňovat za AC jmenovitou hodnotu součástky. Kondenzátor musí být výrobcem určen pro trvalý provoz alespoň při `230 V AC / 50 Hz`; vyšší AC jmenovité napětí vytváří rezervu.
- Fázory budou kontrolovány komplexními čísly. Nebudou zavedeny samostatně označené složky `I_x` a `I_y`.
- Na titulní straně bude skutečné schéma svítidla. Náhradní schéma a fázorový diagram budou v následujících sekcích.

## Chybějící informace

Pro textový návrh nechybí žádný odborný vstup. Osobní a školní údaje titulní strany se převezmou ze schváleného protokolu 2Z.

Správným výpočtovým vzorem je 14. příklad na tiskových stranách 7–8 souboru `priklady_do_cviceni_2026_10_12_LMS.pdf`. Obsahuje stejné zapojení a postup `φ, φ′ → Q_C → I_C → X_C → C_K → napěťové dimenzování → I, I′`.
