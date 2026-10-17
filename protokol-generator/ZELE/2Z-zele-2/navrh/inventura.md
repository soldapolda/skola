# Inventura podkladů – ZELE 2Z

## Zdrojové soubory

- `podklady/Zadání semestrálního projektu ZELE.pdf`
  - obecné pokyny k semestrálnímu projektu;
  - úplný text druhého příkladu;
  - principiální schéma zapojení;
  - vypínací charakteristika jističů B, C a D.
- `podklady/ZELE_Parametry_zadání_SP_Út_17_45-19_15_2.pdf`
  - individuální zadání pro Vojtěcha Solanského;
  - schéma druhého příkladu;
  - parametry spotřebičů a jističe.

Kopie mají shodné kontrolní součty SHA-256 s původními soubory v kořeni projektu. Původní PDF se nebudou upravovat.

## Zadané parametry druhého příkladu

- napájecí napětí: `U = 230 V`;
- frekvence: `f = 50 Hz`;
- jistič: charakteristika `B`, jmenovitý proud `I_n = 16 A`;
- spotřebič 1: `U_n1 = 230 V`, `P_1 = 2300 W`, `cos φ_1 = 1`;
- spotřebič 2: `U_n2 = 230 V`, `P_2 = 220 W`, `cos φ_2 = 0,63`;
- spotřebič 3: `U_n3 = 230 V`, `P_3 = 7000 W`, `cos φ_3 = 0,74`.

## Schválená rozhodnutí

- proud každého spotřebiče se určí ze vztahu `P = U·I·cos φ`, převede se na komplexní fázor a celkový proud se získá součtem komplexních proudů;
- nepoužijí se samostatně označené osové složky `I_x` a `I_y`; výsledný proud se zapíše v algebraickém i polárním tvaru;
- protokol bude obsahovat přesný fázorový diagram jednotlivých proudů a jejich výslednice;
- spotřebiče 2 a 3 se podle motorových značek považují za induktivní;
- titulní údaje navážou na protokol 1Z, označení projektu se změní na `2Z`;
- použije se anotovaný originál vypínací charakteristiky;
- charakteristika dostane vlastní stránku, počet stran není omezen;
- nad charakteristikou budou hodnoty `I`, `I_n`, `I/I_n`, `t_min` a `t_max`;
- dokument nebude obsahovat přístroje, postup měření, naměřené hodnoty ani XLSX.

## Chybějící údaje

Pro sestavení návrhu nechybí žádný nezbytný údaj. Rozběhové proudy motorů, odpory vedení a účinnosti spotřebičů nejsou zadány a nebudou se domýšlet.
