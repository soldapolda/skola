# Finální kontrola protokolu ZELE 4Z

Datum kontroly: 17. 10. 2026

## Zdroj zadání a metoda

- Použit 4. příklad ze souboru `Zadání semestrálního projektu ZELE.pdf`.
- Použity individuální hodnoty `U = 35 V`, `L₁ = 36 mH`, `R₁ = 32 Ω`, `L₂ = 41 mH`, `R₂ = 24 Ω` a `P = 2,1 W`.
- Příklady 11 a 13 ze souboru `priklady_do_cviceni_2026_10_12_LMS.pdf` byly použity pro kontrolu náhradního modelu reálných cívek, reaktance a fázového posuvu.
- Řešení používá schválený napěťový trojúhelník a průběžné zaokrouhlování na tři desetinná místa.

## Matematická kontrola

- Ověřen řetězec `R = 56,000 Ω`, `L = 0,077 H`, `I = 0,194 A`, `U_R = 10,864 V`, `U_L = 33,271 V`, `X_L = 171,500 Ω`, `f = 354,481 Hz` a `φ = 71,917°`.
- Kontrolní výpočet z plné přesnosti dává `f = 355,194336 Hz` a `φ = 71,950492°`; rozdíl odpovídá schválenému použití zaokrouhlených mezivýsledků.
- Zpětné dosazení zobrazeného proudu dává `P = 2,108 W`. Rozdíl `0,008 W`, tedy `0,363 %`, je v dokumentu výslovně vysvětlen.
- Fázový posuv má správný kladný induktivní charakter; proud se za napětím zpožďuje.

## Struktura DOCX

- Balíček DOCX prošel testem integrity bez chyb.
- Dokument obsahuje jednu původní titulní tabulku, jednu pomocnou bezokrajovou tabulku zadaných hodnot, čtyři vložené obrázky, 30 objektů `m:oMath` a 18 bloků `m:oMathPara`.
- Rovnice jsou nativní editovatelné OMML, nikoli obrázky.
- Hlavní schéma, náhradní schéma, fázorový diagram a náhled grafu jsou vloženy jako PNG; samostatné zdrojové SVG schémat a fázorového diagramu jsou zachovány v `vystup/grafika/`.
- Dokument neobsahuje prázdné sekce pro přístroje, postup měření ani naměřené hodnoty.

## Kontrola XLSX

- `graf_P_f.xlsx` prošel testem integrity bez chyb a obsahuje listy `Data`, `Výpočty` a `Graf`.
- Sešit obsahuje skutečný editovatelný bodový XY graf a zdrojovou frekvenční řadu `0–600 Hz`.
- Ověřeny byly vzorce i hodnoty: přesný průsečík `355,194336 Hz`, výsledek protokolu `354,481 Hz` a kontrolní výkon `2,107645 W`.
- Změna vstupního napětí z `35 V` na `36 V` při kontrolním otevření aktualizovala mezivýpočet frekvence i řadu grafu; změna nebyla do souboru uložena.

## Vizuální kontrola

- Dokument byl pomocně vykreslen LibreOffice 7.3 do pěti stran A4.
- Zkontrolovány byly všechny strany: titulní tabulka, hlavní schéma, zadané hodnoty, náhradní schéma, výpočty, nová grafická strana a zhodnocení.
- Nebylo zjištěno přetečení textu, oříznutí rovnic nebo obrázků, rozbití tabulek ani osamocený nadpis.
- Po první kontrole byla opravena poloha označení proudu na titulním schématu, aby se nepřekrývalo s označením `L₁`.
- Pixelové porovnání původního a rozšířeného LibreOffice náhledu potvrdilo nulový rozdíl mezi původními stranami 1–3 a novými stranami 1–3 i mezi původní stranou 4 a novou stranou 5. Jedinou změnou dokumentu je vložená strana 4.
- LibreOffice náhled je pouze předběžná kontrola; vzhled nebyl v tomto prostředí přímo ověřen v Microsoft Wordu. DOCX zachovává sazbu a archetypy závazné wordové předlohy.
