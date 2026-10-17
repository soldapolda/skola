# Kompletní textový návrh protokolu – ZELE 4Z

## TITULNÍ STRANA

- Název měření: `SEMESTRÁLNÍ PROJEKT ZELE 4Z`
- Téma: `Sériové spojení dvou reálných cívek`
- Číslo měření: `4Z`
- Ostatní údaje: převzít ze schválené předlohy.
- Hlavní schéma: zdroj střídavého napětí a sériově zapojené prvky `L₁`, `R₁`, `L₂`, `R₂`.
- Pod schématem uvést všechny zadané hodnoty.

## ZADÁNÍ

Dvě reálné cívky jsou spojeny do série a připojeny ke zdroji střídavého napětí o konstantní efektivní hodnotě a proměnné frekvenci. Mezi cívkami není žádná vzájemná magnetická vazba.

Vypočítejte frekvenci, při které je celkový činný výkon obvodu roven zadané hodnotě. Dále určete proud obvodem a fázový posuv mezi napájecím napětím a proudem.

### Zadané hodnoty

`U = 35 V`, `L₁ = 36 mH`, `R₁ = 32 Ω`, `L₂ = 41 mH`, `R₂ = 24 Ω`, `P = 2,1 W`.

## NÁHRADNÍ SCHÉMA

Obě cívky se nahradí jedním sériovým obvodem s celkovým odporem `R = R₁ + R₂` a celkovou indukčností `L = L₁ + L₂`.

## VÝPOČTY

Všechny zobrazené mezivýsledky se zaokrouhlují na tři desetinná místa a v této podobě se použijí v následujícím kroku.

1. `R = 56,000 Ω`
2. `L = 77,000 mH = 0,077 H`
3. `I = √(P/R) = 0,194 A`
4. `U_R = RI = 10,864 V`
5. `U_L = √(U² − U_R²) = 33,271 V`
6. `X_L = U_L/I = 171,500 Ω`
7. `f = X_L/(2πL) = 354,481 Hz`
8. `φ = arctan(U_L/U_R) = 71,917°`

Obvod má induktivní charakter. Napájecí napětí předbíhá proud, respektive proud se za napětím zpožďuje o `71,917°`.

## SAMOSTATNÁ STRANA 4 – FÁZOROVÝ DIAGRAM A GRAF

- Fázorový diagram zachovává poměry `U_R = 10,864 V`, `U_L = 33,271 V`, `U = 35,000 V` a úhel `φ = 71,917°`.
- Graf používá vztah `P(f) = U²R / (R² + (2πfL)²)` v rozsahu `0–600 Hz`.
- V grafu jsou označeny body `355,194 Hz; 2,100 W` a `354,481 Hz; 2,108 W`.
- Zdrojová data, mezivýpočty, vzorce a editovatelný graf jsou zachovány v `graf_P_f.xlsx`.
- Tato stránka se vloží mezi výpočty a zhodnocení. Ostatní strany se obsahově ani vizuálně nemění.

## ZHODNOCENÍ

Pro sériové spojení dvou reálných cívek byla stanovena výsledná frekvence `f = 354,481 Hz`, při které je podle použitého modelu celkový činný výkon `2,1 W`. Proud obvodem je `I = 0,194 A`.

Celkový fázový posuv je `φ = 71,917°`. Obvod má odporově-induktivní charakter, a proto se proud za napájecím napětím zpožďuje. Výpočet předpokládá lineární parametry cívek a nulovou vzájemnou magnetickou vazbu.

Kontrolní dosazení zobrazeného proudu dává `P = I²R = 2,108 W`. Rozdíl `0,008 W`, tedy přibližně `0,363 %`, je způsoben schváleným průběžným zaokrouhlováním.

Jde o teoretický výsledek bez experimentálního ověření. Model nezohledňuje frekvenční závislost odporů, parazitní kapacity, ztráty v magnetických obvodech ani tolerance cívek.
