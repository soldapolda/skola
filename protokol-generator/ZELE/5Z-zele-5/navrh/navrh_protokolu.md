# Kompletní textový návrh protokolu – ZELE 5Z

Tento soubor je určen ke společnému schválení celého obsahu před vytvořením DOCX a grafických podkladů.

## TITULNÍ STRANA

- Název měření: `SEMESTRÁLNÍ PROJEKT ZELE 5Z`
- Zkoušené předměty / téma: `Kompenzace účiníku zářivkového svítidla`
- Číslo měření: `5Z`
- Ostatní osobní a školní údaje: převzít beze změny ze schváleného protokolu 2Z.
- Hlavní schéma: skutečné zapojení zářivkového svítidla s tlumivkou, trubicí, startérem a paralelním kompenzačním kondenzátorem `C_K`.
- Pod schématem uvést hodnoty `U = 230 V`, `f = 50 Hz`, `P = 30 W`, `cos(φ) = 0,31` a `cos(φ′) = 0,95`.

---

## ZADÁNÍ

Klasické zářivkové svítidlo je tvořeno zářivkovou trubicí, tlumivkou a startérem. Zářivková trubice spolu s tlumivkou se v ustáleném stavu chová jako odporově-induktivní zátěž. Parazitní vlastnosti a nelinearity se v teoretickém modelu zanedbávají. Startér sepne pouze na okamžik při zapnutí a při běžném svícení je rozepnutý.

Kompenzační kondenzátor není pro samotnou funkci svítidla nezbytný. Jeho úlohou je zmenšit induktivní jalový odběr svítidla, a tím zvýšit jeho účiník. Pro svítidlo se zadaným činným výkonem a původním účiníkem se navrhne kapacita paralelního kompenzačního kondenzátoru tak, aby byl po kompenzaci dosažen požadovaný účiník.

Určete:

1. kapacitu kompenzačního kondenzátoru `C_K`;
2. minimální jmenovité napětí kondenzátoru `U_nC`;
3. proud svítidla bez kompenzace `I`;
4. proud svítidla po kompenzaci `I′`;
5. fázorový diagram napájecího napětí a proudů před kompenzací a po ní.

### Zadané hodnoty

\[
U=230\ \mathrm{V}, \qquad f=50\ \mathrm{Hz}, \qquad P=30\ \mathrm{W}
\]

\[
\cos(\varphi)=0{,}31, \qquad \cos(\varphi')=0{,}95
\]

---

## NÁHRADNÍ SCHÉMA

Zářivková trubice s tlumivkou bude nahrazena sériovou odporově-induktivní větví `R–X_L`. Kompenzační kondenzátor `C_K` bude připojen paralelně k celému svítidlu. Proud původní odporově-induktivní větve bude označen `I`, kapacitní proud `I_C` a celkový proud odebíraný po kompenzaci `I′`. Pro fázory bude platit vztah

\[
\overline I' = \overline I + \overline I_C.
\]

---

## VÝPOČTY

Všechny zobrazené mezivýsledky se zaokrouhlí na tři desetinná místa a v této podobě se použijí v následujícím kroku.

### Fázové posuvy před kompenzací a po kompenzaci

\[
\varphi=\arccos(\cos\varphi)
\qquad
\varphi=\arccos(0{,}31)
\]

\[
\mathbf{\varphi=71{,}941^\circ}
\]

\[
\varphi'=\arccos(\cos\varphi')
\qquad
\varphi'=\arccos(0{,}95)
\]

\[
\mathbf{\varphi'=18{,}195^\circ}
\]

### Potřebný jalový výkon kompenzačního kondenzátoru

\[
Q_C=P\left(\tan\varphi-\tan\varphi'\right)
\qquad
Q_C=30\left(\tan71{,}941^\circ-\tan18{,}195^\circ\right)
\]

\[
\mathbf{Q_C=82{,}147\ \mathrm{var}}
\]

### Proud kompenzačního kondenzátoru

\[
I_C=\frac{Q_C}{U}
\qquad
I_C=\frac{82{,}147}{230}
\]

\[
\mathbf{I_C=0{,}357\ \mathrm{A}}
\]

### Kapacitní reaktance

\[
X_C=\frac{U}{I_C}
\qquad
X_C=\frac{230}{0{,}357}
\]

\[
\mathbf{X_C=644{,}258\ \Omega}
\]

### Kapacita kompenzačního kondenzátoru

\[
\omega=2\pi f
\qquad
\omega=2\pi\cdot50
\]

\[
\mathbf{\omega=314{,}159\ \mathrm{rad\cdot s^{-1}}}
\]

\[
X_C=\frac{1}{\omega C_K}
\qquad
C_K=\frac{1}{\omega X_C}
\]

\[
C_K=\frac{1}{314{,}159\cdot644{,}258}
\]

\[
\mathbf{C_K=4{,}941\cdot10^{-6}\ \mathrm{F}=4{,}941\ \mu\mathrm{F}}
\]

Jde o teoreticky vypočtenou hodnotu. Praktická normalizovaná kapacita se nebude vybírat, protože to zadání nepožaduje.

### Napěťové dimenzování kondenzátoru

Podle postupu ve vzorovém příkladu se nejprve určí amplituda síťového napětí:

\[
U_m=\sqrt{2}\,U
\qquad
U_m=\sqrt{2}\cdot230
\]

\[
\mathbf{U_m=325{,}269\ \mathrm{V}\approx325\ \mathrm{V}}
\]

Hodnota `325,269 V` je maximální okamžitá hodnota sinusového napájecího napětí, nikoli jmenovitá efektivní hodnota pro střídavý provoz uvedená na kondenzátoru. Kompenzační kondenzátor musí být výrobcem výslovně určen pro trvalý provoz alespoň při `230 V AC / 50 Hz`; jeho izolace přitom musí bezpečně snášet vypočtenou amplitudu a provozní přepětí. Vyšší AC jmenovité napětí vytváří vhodnou rezervu. Vhodný je fóliový kondenzátor pro kompenzaci účiníku, nikoli běžný polarizovaný elektrolytický kondenzátor.

### Proud svítidla bez kompenzace

\[
I=\frac{P}{U\cos\varphi}
\qquad
I=\frac{30}{230\cdot0{,}31}
\]

\[
\mathbf{I=0{,}421\ \mathrm{A}}
\]

### Proud svítidla po kompenzaci

\[
I'=\frac{P}{U\cos\varphi'}
\qquad
I'=\frac{30}{230\cdot0{,}95}
\]

\[
\mathbf{I'=0{,}137\ \mathrm{A}}
\]

### Komplexní kontrola proudů

Původní induktivní jalový výkon a jalový výkon po kompenzaci jsou

\[
Q=P\tan\varphi
\qquad
Q=30\tan71{,}941^\circ
\]

\[
\mathbf{Q=92{,}008\ \mathrm{var}}
\]

\[
Q'=Q-Q_C
\qquad
Q'=92{,}008-82{,}147
\]

\[
\mathbf{Q'=9{,}861\ \mathrm{var}}
\]

Napájecí napětí se zvolí jako referenční fázor. Induktivní proud má zápornou imaginární složku a kapacitní proud kladnou imaginární složku:

\[
\overline I=\frac{P}{U}-j\frac{Q}{U}
\qquad
\overline I=\frac{30}{230}-j\frac{92{,}008}{230}
\]

\[
\mathbf{\overline I=0{,}130-j0{,}400\ \mathrm{A}}
\]

\[
\overline I_C=j\frac{Q_C}{U}
\qquad
\mathbf{\overline I_C=j0{,}357\ \mathrm{A}}
\]

\[
\overline I'=\overline I+\overline I_C
\]

\[
\overline I'=(0{,}130-j0{,}400)+j0{,}357
\]

\[
\mathbf{\overline I'=0{,}130-j0{,}043\ \mathrm{A}}
\]

Velikosti komplexních proudů po zaokrouhlení potvrzují výsledky `I = 0,421 A` a `I′ = 0,137 A`. Drobná odchylka úhlu vypočteného pouze ze zobrazených komplexních složek je důsledkem jejich průběžného zaokrouhlení.

---

## FÁZOROVÝ DIAGRAM

Diagram bude vytvořen jako přesná vektorová konstrukce podle měřítek ze zadání:

- napětí: `1 mm ≙ 6 V`;
- proudy: `1 mm ≙ 0,02 A`.

Referenční fázor napětí `U` bude vodorovně doprava. Proud `I` bude za napětím zaostávat o `71,941°`, kapacitní proud `I_C` bude napětí předbíhat o `90°` a proud po kompenzaci `I′` bude zaostávat o `18,195°`. Konstrukce bude zachovávat vztah `Ī′ = Ī + Ī_C`.

Orientační délky v diagramu jsou:

- `U`: `230/6 = 38,333 mm`;
- `I`: `0,421/0,02 = 21,050 mm`;
- `I_C`: `0,357/0,02 = 17,850 mm`;
- `I′`: `0,137/0,02 = 6,850 mm`.

Pro geometrickou konstrukci budou použity nezaokrouhlené interní hodnoty, aby se vektory přesně uzavřely; popisky budou odpovídat schváleným třídesetinným výsledkům.

---

## ZHODNOCENÍ

Pro zářivkové svítidlo s činným výkonem `30 W` a původním účiníkem `0,31` byla vypočtena teoretická kapacita paralelního kompenzačního kondenzátoru `C_K = 4,941 µF`. Amplituda napájecího napětí je `325,269 V`. Tato hodnota není AC jmenovitý údaj kondenzátoru; součástka musí být výrobcem určena pro trvalý provoz alespoň při `230 V AC / 50 Hz`, bezpečně snášet uvedenou amplitudu a mít vhodnou napěťovou rezervu.

Proud odebíraný svítidlem bez kompenzace je `0,421 A`. Po zvýšení účiníku na `0,95` klesne proud odebíraný ze sítě na `0,137 A`. Činný výkon svítidla zůstává `30 W`; kompenzační kondenzátor pouze zmenšuje induktivní jalovou složku proudu. Tím se zmenší proudové zatížení vedení a související ztráty.

Komplexní kontrola potvrdila, že kapacitní proud `j0,357 A` zmenší imaginární složku původního proudu z přibližně `−j0,400 A` na `−j0,043 A`. Výsledný proud proto svírá s napájecím napětím podstatně menší fázový úhel.

Výsledky popisují idealizovaný teoretický model. Nebyly experimentálně ověřeny a nezahrnují nelinearity zářivkové trubice, parazitní vlastnosti tlumivky, tolerance kondenzátoru ani změny napájecího napětí.
