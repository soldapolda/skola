# Kompletní textový návrh protokolu – ZELE 3Z

## TITULNÍ STRANA

- Název měření: `SEMESTRÁLNÍ PROJEKT ZELE 3Z`
- Téma: `Trojfázový asynchronní motor`
- Číslo měření: `3Z`
- Ostatní údaje: převzít ze schválené předlohy.
- Hlavní grafický prvek: technické zobrazení třífázového asynchronního motoru.
- Pod zobrazením uvést všechny zadané hodnoty.

## ZADÁNÍ

Trojfázový asynchronní motor pracuje při jmenovitém napětí `U_n` a jmenovité frekvenci `f_n`. Ze zadaných štítkových a katalogových údajů určete synchronní otáčky `n_S`, otáčky při zatížení polovinou jmenovitého momentu `n_X`, jmenovitý moment `M_n`, záběrný proud `I_z`, záběrný moment `M_z` a jmenovitou účinnost `η_n`.

Přiložená momentová charakteristika je pouze orientační. Její hodnoty se nesmějí odměřovat; pro výpočet otáček při polovičním momentu se použije přibližně lineární pracovní oblast motoru.

### Zadané hodnoty

`U_n = 400 V`, `f_n = 50 Hz`, `2p = 2`, `P_n = 7200 W`, `n_n = 2951 min⁻¹`, `I_n = 13 A`, `cos(φ_n) = 0,88`, `M_z/M_n = 2,1`, `I_z/I_n = 9`.

## MOMENTOVÁ CHARAKTERISTIKA

Vložit přesný výřez původního orientačního náčrtku ze zadání. Náčrtek slouží pouze k vysvětlení tvaru běžné pracovní oblasti a nebude použit pro odečet číselných hodnot.

## VÝPOČTY

Všechny zobrazené mezivýsledky se zaokrouhlují na tři desetinná místa a v této podobě se použijí v následujícím kroku.

### Počet pólových dvojic

`p = 2p/2 = 2/2 = 1`

### Synchronní otáčky

`n_S = 60f_n/p = (60·50)/1 = 3000,000 min⁻¹`

### Jmenovitá účinnost

`η_n = P_n/(√3·U_n·I_n·cos(φ_n))·100`

`η_n = 7200/(√3·400·13·0,88)·100 = 90,842 %`

### Záběrný proud

`I_z = I_n·(I_z/I_n) = 13·9 = 117,000 A`

### Jmenovitý moment

`M_n = P_n/(2πn_n/60) = P_n·60/(2πn_n)`

`M_n = (7200·60)/(2π·2951) = 23,299 N·m`

### Záběrný moment

`M_z = M_n·(M_z/M_n) = 23,299·2,1 = 48,928 N·m`

### Otáčky při polovině jmenovitého momentu

V běžné pracovní oblasti se použije přibližně lineární vztah

`(n_S − n_X)/M_X = (n_S − n_n)/M_n`.

Protože `M_X = 0,5M_n`, platí

`n_X = n_S − 0,5(n_S − n_n)`

`n_X = 3000 − 0,5(3000 − 2951) = 2975,500 min⁻¹`.

## ZHODNOCENÍ

Dvoupólovému asynchronnímu motoru napájenému frekvencí `50 Hz` odpovídají synchronní otáčky `n_S = 3000,000 min⁻¹`. Jmenovité otáčky `2951 min⁻¹` jsou nižší, protože motor při zatížení pracuje se skluzem.

Při zatížení polovinou jmenovitého momentu vycházejí z lineární aproximace běžné pracovní oblasti otáčky `n_X = 2975,500 min⁻¹`. Tato hodnota nebyla odečtena z orientačního náčrtku.

Jmenovitý moment motoru je `M_n = 23,299 N·m`. Záběrný proud `I_z = 117,000 A` je devítinásobkem jmenovitého proudu a záběrný moment `M_z = 48,928 N·m` je 2,1násobkem jmenovitého momentu. Jmenovitá účinnost vychází `η_n = 90,842 %`.

Výsledky popisují idealizovaný teoretický výpočet z jmenovitých a katalogových údajů. Nebyly experimentálně ověřeny a nezohledňují toleranci parametrů, změnu napájecího napětí, zahřívání ani nelinearity skutečné momentové charakteristiky mimo běžnou pracovní oblast.
