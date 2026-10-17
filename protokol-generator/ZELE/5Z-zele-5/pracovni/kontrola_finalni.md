# Finální kontrola protokolu 5Z

Datum kontroly: 17. 10. 2026

## Zdroj zadání a postup řešení

- Použito zadání `5. Příklad` ze souboru `Zadání semestrálního projektu ZELE.pdf`.
- Použity individuální hodnoty `U = 230 V`, `f = 50 Hz`, `P = 30 W`, `cos(φ) = 0,31` a `cos(φ′) = 0,95` ze souboru `ZELE_Parametry_zadání_SP_Út_17_45-19_15_2.pdf`.
- Jako vzor postupu byl ověřen `14. Příklad` na tištěných stranách 7–8 souboru `priklady_do_cviceni_2026_10_12_LMS.pdf`.
- Zachované pořadí postupu: fázové posuvy → potřebný jalový výkon → proud kondenzátoru → kapacitní reaktance → kapacita → napěťové dimenzování → proudy před a po kompenzaci.

## Matematická kontrola

- Ověřeno průběžné zaokrouhlování každého zobrazeného mezivýsledku na tři desetinná místa.
- Ověřen řetězec výsledků: `φ = 71,941°`, `φ′ = 18,195°`, `Q_C = 82,147 var`, `I_C = 0,357 A`, `X_C = 644,258 Ω`, `ω = 314,159 rad·s⁻¹`, `C_K = 4,941 µF`, `U_m = 325,269 V`, `I = 0,421 A`, `I′ = 0,137 A`, `Q = 92,008 var` a `Q′ = 9,861 var`.
- Ověřena komplexní kontrola: `Ī = 0,130 − j0,400 A`, `Ī_C = j0,357 A`, `Ī′ = 0,130 − j0,043 A`.
- Výpočet `U_m = √2·U = 325,269 V` je výslovně označen jako amplituda napájecího napětí. Text samostatně uvádí požadavek na kondenzátor určený pro trvalý provoz alespoň při `230 V AC / 50 Hz`, včetně napěťové rezervy a odolnosti proti provozním přepětím.
- Geometrie fázorového diagramu je vytvořena z nezaokrouhlených hodnot; viditelné popisky jsou zaokrouhleny na tři desetinná místa.

## Struktura DOCX

- Balíček DOCX prošel testem integrity bez chyb.
- Dokument obsahuje 32 bloků `m:oMathPara` a 42 objektů `m:oMath`; výpočty jsou tedy vloženy jako nativní editovatelné rovnice Wordu, nikoli jako obrázky.
- Dokument obsahuje tři vložené grafické objekty: hlavní schéma, náhradní schéma a fázorový diagram.
- Zdrojové varianty PNG a SVG jsou zachovány v `vystup/grafika/`.
- V DOCX nejsou vloženy žádné prázdné sekce pro měření, přístroje ani graf, protože jde o teoretickou úlohu.

## Vizuální kontrola

- Dokument byl pomocně vykreslen LibreOffice 7.3 do pěti stran A4.
- Vizuálně byly zkontrolovány všechny strany: titulní tabulka, hlavní schéma, zadané hodnoty, náhradní schéma, výpočty, fázorový diagram a zhodnocení.
- Nebylo zjištěno přetečení textu, oříznutí rovnic nebo obrázků, rozbití tabulek ani osamocený nadpis na konci stránky.
- LibreOffice náhled je pouze předběžná kontrola. Vzhled v Microsoft Wordu nebyl na tomto Linuxu přímo ověřen; DOCX proto zachovává sazbu a archetypy rovnic ze závazného wordového vzoru.

