# Struktura projektu a protokolu

## Projektové adresáře

```text
protokol-generator/
├── AGENTS.md
├── vzory/
├── pravidla/
├── mereni/
│   └── <identifikator_mereni>/
│       ├── podklady/
│       │   ├── zadani/
│       │   ├── vypocty/
│       │   ├── schemata/
│       │   ├── hodnoty/
│       │   └── prilohy/
│       ├── navrh/
│       │   ├── inventura.md
│       │   └── navrh_protokolu.md
│       ├── pracovni/
│       └── vystup/
│           ├── protokol.docx
│           ├── graf.xlsx
│           ├── kontrolni_nahled.pdf
│           ├── grafy/
│           └── schemata/
└── pomocne_nastroje/
```

Adresáře a soubory, které nejsou pro konkrétní měření potřeba, není nutné vytvářet.

## Univerzální struktura protokolu

### Titulní strana

- školní a identifikační údaje;
- přesně jedno hlavní schéma;
- poznámky učitele, známka a datum.

### Jádro měřicího protokolu

1. ÚKOL MĚŘENÍ
2. POUŽITÉ PŘÍSTROJE
3. POSTUP MĚŘENÍ
4. PŘÍKLAD VÝPOČTU
5. ZHODNOCENÍ

### Jádro čistě teoretického projektu

1. ZADÁNÍ
2. Zadané hodnoty
3. NÁHRADNÍ SCHÉMA, pokud je potřebné k odvození
4. VÝPOČTY
5. ZHODNOCENÍ

Sekce přístrojů, postupu měření, naměřených hodnot a grafů se vynechají, pokud nebylo provedeno měření a zadání je nevyžaduje.

Sekce `ÚVOD` není automatická. Zařadí se pouze na základě zadání nebo schváleného návrhu. Pokud se v libovolném typu protokolu objeví některá ze sekcí obsažených ve `vzor_vypoctovych_sekci.docx`, její sazba a vnitřní struktura se řídí tímto vzorem; ostatní sekce se volí individuálně.

### Podmíněné sekce

- TABULKA NAMĚŘENÝCH A VYPOČTENÝCH HODNOT
- NÁHRADNÍ SCHÉMA
- GRAFY
- FÁZOROVÝ DIAGRAM
- ODVŮVODNĚNÍ NEBO ODVOZENÍ VZTAHŮ
- PŘÍLOHY

Pořadí podmíněných sekcí se volí podle logiky konkrétního měření. Tabulka hodnot obvykle následuje po postupu a před příklady výpočtů. Náhradní schéma se umístí co nejblíže výpočtu, pro který je potřeba.

Graf má vlastní celou stránku. Jsou-li grafy dva, přednostně se umístí společně na jednu stránku, pokud zůstanou čitelné.
