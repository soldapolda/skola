# Kompletní návrh protokolu – ZELE 2Z

Tento soubor obsahuje celý navržený obsah před sazbou do Wordu. Rovnice budou ve výsledném DOCX vytvořeny jako nativní editovatelné OMML podle ručně schváleného vzoru 1Z.

## TITULNÍ STRANA

### Identifikační pole

- Jméno: Vojtěch Solanský
- Název měření: **SEMESTRÁLNÍ PROJEKT ZELE 2Z**
- Třída: T4A
- Skupina: 3
- Číslo měření: **2Z**
- Zkoušené předměty: **Střídavý rozvod jištěný jističem**
- Změřeno dne: 9. 9. 2025
- Vyučující: Vladimír Kokeš
- Funkce při měření: Zapojující, Měřič
- Spoluměřící: -

### Schéma a hodnoty

Do pole `Schéma` bude vloženo principiální schéma zdroje 230 V, jističe a tří paralelně připojených spotřebičů. Pod schématem budou ve třech sloupcích uvedeny parametry spotřebičů a samostatně označení jističe B16.

---

## ZADÁNÍ

Střídavý rozvod je napájen ze zdroje konstantního střídavého napětí 230 V o frekvenci 50 Hz. Rozvod je jištěn jističem se jmenovitým proudem 16 A a vypínací charakteristikou B. K rozvodu jsou paralelně připojeny tři spotřebiče se zadanými činnými výkony a účiníky.

Úkolem je vypočítat celkový proud protékající jističem, určit, zda jistič vypne, a v případě vypnutí odečíst z dodané vypínací charakteristiky minimální a maximální vypínací čas.

### Zadané hodnoty

**Napájecí zdroj a jistič**

\[
U=230\ \mathrm{V}, \qquad f=50\ \mathrm{Hz}, \qquad I_n=16\ \mathrm{A}, \qquad \text{charakteristika B}
\]

**Spotřebič 1**

\[
U_{n1}=230\ \mathrm{V}, \qquad P_1=2300\ \mathrm{W}, \qquad \cos\varphi_1=1
\]

**Spotřebič 2**

\[
U_{n2}=230\ \mathrm{V}, \qquad P_2=220\ \mathrm{W}, \qquad \cos\varphi_2=0{,}63
\]

**Spotřebič 3**

\[
U_{n3}=230\ \mathrm{V}, \qquad P_3=7000\ \mathrm{W}, \qquad \cos\varphi_3=0{,}74
\]

## NÁHRADNÍ SCHÉMA

Pro výpočet jsou všechny tři spotřebiče uvažovány jako paralelně připojené k ideálnímu zdroji napětí 230 V. Spotřebič 1 má jednotkový účiník. Spotřebiče 2 a 3 jsou podle značek motorů považovány za induktivní zátěže. Celkový proud jističem je proto nutné určit fázorovým součtem proudů, nikoli prostým součtem jejich velikostí.

Pod tímto odstavcem bude vloženo principiální schéma z individuálního zadání s vyznačeným směrem celkového proudu `I`.

---

## VÝPOČTY

Při výpočtu proudu jednotlivých spotřebičů se vychází ze vztahu pro činný výkon střídavého jednofázového spotřebiče:

\[
P=U\cdot I\cdot\cos\varphi
\]

Z tohoto vztahu se vyjádří proud:

\[
I=\frac{P}{U\cdot\cos\varphi}
\]

Protože mají spotřebiče rozdílné fázové posuny a účiníky, nelze velikosti jejich proudů prostě aritmeticky sečíst. Napětí se zvolí jako referenční fázor

\[
\underline U=230\angle0^\circ\ \mathrm{V}
\]

a jednotlivé proudy se zapíší jako komplexní fázory. Spotřebiče 2 a 3 jsou induktivní, jejich proudy proto zaostávají za napětím a mají záporný fázový úhel i zápornou imaginární část. Všechny zobrazené mezivýsledky jsou zaokrouhleny na tři desetinná místa a v této podobě použity v následujících krocích.

### Spotřebič 1

Proud spotřebiče:

\[
I_1=\frac{P_1}{U\cdot\cos\varphi_1}
\qquad
I_1=\frac{2300}{230\cdot1}
\]

\[
\mathbf{I_1=10{,}000\ \mathrm{A}}
\]

Fázový posun:

\[
\varphi_1=\arccos(\cos\varphi_1)
\qquad
\varphi_1=\arccos(1)
\]

\[
\mathbf{\varphi_1=0{,}000^\circ}
\]

Komplexní fázor proudu:

\[
\underline I_1=I_1\left(\cos\varphi_1-j\sin\varphi_1\right)
\qquad
\underline I_1=10{,}000\left(\cos0{,}000^\circ-j\sin0{,}000^\circ\right)
\]

\[
\mathbf{\underline I_1=10{,}000+j0{,}000\ \mathrm{A}}
\]

### Spotřebič 2

Proud spotřebiče:

\[
I_2=\frac{P_2}{U\cdot\cos\varphi_2}
\qquad
I_2=\frac{220}{230\cdot0{,}63}
\]

\[
\mathbf{I_2=1{,}518\ \mathrm{A}}
\]

Fázový posun:

\[
\varphi_2=\arccos(\cos\varphi_2)
\qquad
\varphi_2=\arccos(0{,}63)
\]

\[
\mathbf{\varphi_2=50{,}950^\circ}
\]

Komplexní fázor proudu:

\[
\underline I_2=I_2\left(\cos\varphi_2-j\sin\varphi_2\right)
\]

\[
\underline I_2=1{,}518\left(\cos50{,}950^\circ-j\sin50{,}950^\circ\right)
\]

\[
\mathbf{\underline I_2=0{,}956-j1{,}179\ \mathrm{A}}
\]

### Spotřebič 3

Proud spotřebiče:

\[
I_3=\frac{P_3}{U\cdot\cos\varphi_3}
\qquad
I_3=\frac{7000}{230\cdot0{,}74}
\]

\[
\mathbf{I_3=41{,}128\ \mathrm{A}}
\]

Fázový posun:

\[
\varphi_3=\arccos(\cos\varphi_3)
\qquad
\varphi_3=\arccos(0{,}74)
\]

\[
\mathbf{\varphi_3=42{,}269^\circ}
\]

Komplexní fázor proudu:

\[
\underline I_3=I_3\left(\cos\varphi_3-j\sin\varphi_3\right)
\]

\[
\underline I_3=41{,}128\left(\cos42{,}269^\circ-j\sin42{,}269^\circ\right)
\]

\[
\mathbf{\underline I_3=30{,}435-j27{,}663\ \mathrm{A}}
\]

### Celkový proud jističem

Komplexní proudy jednotlivých spotřebičů se sečtou:

\[
\underline I=\underline I_1+\underline I_2+\underline I_3
\]

\[
\underline I=(10{,}000+j0{,}000)+(0{,}956-j1{,}179)+(30{,}435-j27{,}663)
\]

\[
\mathbf{\underline I=41{,}391-j28{,}842\ \mathrm{A}}
\]

Velikost výsledného proudu:

\[
I=\left|\underline I\right|
\qquad
I=\sqrt{41{,}391^2+(-28{,}842)^2}
\]

\[
\mathbf{I=50{,}449\ \mathrm{A}}
\]

Fázový posun výsledného proudu:

\[
\varphi_I=\operatorname{atan2}\left(\operatorname{Im}\underline I;\operatorname{Re}\underline I\right)
\qquad
\varphi_I=\operatorname{atan2}(-28{,}842;41{,}391)
\]

\[
\mathbf{\varphi_I=-34{,}869^\circ}
\]

Výsledný proud v polárním tvaru:

\[
\mathbf{\underline I=50{,}449\angle-34{,}869^\circ\ \mathrm{A}}
\]

### Fázorový diagram proudů

Za výpočtem bude vložen přesný fázorový diagram proudů `I₁`, `I₂`, `I₃` a výsledného proudu `I`. Všechny vektory budou vycházet ze společného počátku a budou zakresleny vůči referenčnímu napětí se skutečnými úhly `0°`, `−50,950°`, `−42,269°` a `−34,869°`. Diagram nebude používat samostatně označené složky `I_x` a `I_y`. Jednotné měřítko bude přibližně `2 mm ≙ 1 A` a výsledný proud bude zvýrazněn silnější čarou.

### Posouzení jističe

Násobek jmenovitého proudu jističe:

\[
k=\frac{I}{I_n}
\qquad
k=\frac{50{,}449}{16}
\]

\[
\mathbf{k=3{,}153}
\]

Proud jističem je 3,153násobkem jeho jmenovitého proudu. Jistič B16 proto vypne.

---

## VYPÍNACÍ CHARAKTERISTIKA JISTIČE

Nad grafem bude uvedeno `Velikost nadproudu: 3,153` a následující odečtené hodnoty:

\[
\mathbf{t_{\min}\approx6\ \mathrm{s}}, \qquad
\mathbf{t_{\max}\approx21\ \mathrm{s}}
\]

Do originální vypínací charakteristiky bude zakreslena svislá konstrukční čára v poloze `I/I_n = 3,153` a vodorovné čáry k přibližným mezním časům. Odečet je grafický a odpovídá šířce tolerančního pásma charakteristiky B.

---

## ZHODNOCENÍ

Výpočtem byly stanoveny proudy jednotlivých spotřebičů. Spotřebičem 1 protéká proud 10,000 A, spotřebičem 2 proud 1,518 A a spotřebičem 3 proud 41,128 A. Protože spotřebiče mají rozdílné účiníky a fázové posuny, nebyly velikosti proudů aritmeticky sečteny. Jednotlivé proudy byly převedeny na komplexní fázory a jejich součtem byl získán výsledný proud `41,391 − j28,842 A`, tedy `50,449∠−34,869° A`.

Jmenovitý proud jističe je 16 A, takže skutečný proud představuje 3,153násobek jeho jmenovité hodnoty. Jistič s charakteristikou B při tomto zatížení vypne. Po opravě polohy konstrukční svislice v logaritmické ose byl z dodané charakteristiky odečten minimální čas přibližně 6 s a maximální čas přibližně 21 s. Svislice pro nadproud 3,153 protíná tepelnou část tolerančního pásma B, nikoli okamžitou elektromagnetickou oblast.

Výpočet popisuje ustálený teoretický stav při konstantním napětí 230 V. Neuvažuje úbytky napětí na vedení ani rozběhové proudy motorů, protože tyto hodnoty nebyly zadány. Skutečný okamžik vypnutí by dále ovlivnila počáteční teplota jističe, výrobní tolerance a předchozí zatížení.
