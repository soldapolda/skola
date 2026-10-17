# Finální kontrola protokolu 3Z

Datum kontroly: 17. 10. 2026

## Zdroj zadání a vzor postupu

- Použito zadání `3. Příklad` ze souboru `Zadání semestrálního projektu ZELE.pdf`.
- Použity individuální hodnoty `U_n = 400 V`, `f_n = 50 Hz`, `2p = 2`, `P_n = 7200 W`, `n_n = 2951 min⁻¹`, `I_n = 13 A`, `cos(φ_n) = 0,88`, `M_z/M_n = 2,1` a `I_z/I_n = 9`.
- Jako hlavní vzor výpočtu byl ověřen `24. Příklad` v souboru `priklady_do_cviceni_2026_10_12_LMS.pdf`.
- Pro výpočet otáček při polovině jmenovitého momentu byla použita lineární pracovní oblast podle `25. Příkladu`.
- V dokumentu není tvrzeno zapojení motoru do hvězdy ani do trojúhelníku, protože je individuální zadání neurčuje.

## Matematická kontrola

- Nezávisle byly ověřeny všechny obecné vztahy, dosazení, jednotky a aritmetika.
- Ověřeno průběžné zaokrouhlování zobrazených mezivýsledků na tři desetinná místa.
- Závazné výsledky: `n_S = 3000,000 min⁻¹`, `n_X = 2975,500 min⁻¹`, `M_n = 23,299 N·m`, `I_z = 117,000 A`, `M_z = 48,928 N·m` a `η_n = 90,842 %`.
- Záběrný moment byl vypočten ze zobrazené průběžně zaokrouhlené hodnoty `M_n = 23,299 N·m`.
- Poměr pro poloviční zatěžovací moment je přesně `M_X/M_n = 0,5`; výsledek `n_X` nebyl odečten z náčrtku.

## Grafické podklady

- Titulní strana obsahuje technické zobrazení třífázového asynchronního motoru; zachován je samostatný zdroj `motor.svg` a kompatibilní PNG o rozlišení `1800 × 850 px`.
- Momentová charakteristika je přesný výřez třetí stránky původního zadání, včetně pravých popisků a spodní osy. PNG má rozlišení `2247 × 939 px` při 300 dpi.
- Charakteristika je výslovně označena jako orientační a není prezentována jako graf vytvořený z číselných dat. XLSX proto nebyl vytvořen.

## Struktura DOCX

- Balíček DOCX prošel testem integrity bez chyb.
- Dokument obsahuje 16 bloků `m:oMathPara` a 34 objektů `m:oMath`; výpočty jsou vloženy jako nativní editovatelné rovnice Wordu.
- Dokument obsahuje dvě vložené grafiky: technické zobrazení motoru a původní momentovou charakteristiku.
- Zachována je titulní tabulka, její slučování buněk, ohraničení, písma a rozložení schváleného vzoru.

## Vizuální kontrola

- Dokument byl pomocně vykreslen LibreOffice 7.3 na čtyři strany A4.
- Vizuálně byly zkontrolovány všechny strany: titulní tabulka, motor, zadané hodnoty, úplnost charakteristiky, výpočty a zhodnocení.
- Nebylo zjištěno přetečení textu, oříznutí grafiky, rozbití tabulek, chybějící obrázek ani osamocený nadpis.
- LibreOffice náhled je pouze pomocná kontrola. Dokument nebyl na tomto Linuxu přímo otevřen v Microsoft Wordu; DOCX zachovává sazbu a OMML archetypy závazné wordové předlohy.

