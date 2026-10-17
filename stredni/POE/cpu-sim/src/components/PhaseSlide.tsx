interface PanelProps {
  title: string;
  titleStep: number;
  bullets: string[];
  bulletSteps: number[];
  step: number;
  accentColor: string;
  bgColor: string;
  borderColor: string;
}

function PhasePanel({
  title, titleStep, bullets, bulletSteps, step,
  accentColor, bgColor, borderColor,
}: PanelProps) {
  return (
    <div style={{
      flex: 1,
      backgroundColor: bgColor,
      border: `4px solid ${borderColor}`,
      borderRadius: '1.5vw',
      padding: '2vw',
      display: 'flex',
      flexDirection: 'column',
      gap: '1.2vh',
    }}>
      {/* Phase title */}
      <h2 style={{
        fontSize: '2.2vw',
        fontWeight: 900,
        color: accentColor,
        borderBottom: `3px solid ${accentColor}`,
        paddingBottom: '0.6vh',
        marginBottom: '0.4vh',
        opacity: step >= titleStep ? 1 : 0,
        transform: step >= titleStep ? 'translateX(0)' : 'translateX(-20px)',
        transition: 'opacity 0.35s ease, transform 0.35s ease',
      }}>
        {title}
      </h2>

      {/* Bullets */}
      {bullets.map((text, i) => {
        const threshold = bulletSteps[i];
        const visible  = step >= threshold;
        const isActive = step === threshold;
        return (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.7vw',
              padding: '0.6vh 0.7vw',
              borderRadius: '0.6vw',
              backgroundColor: isActive ? `${accentColor}22` : 'transparent',
              opacity: visible ? 1 : 0,
              transform: visible ? 'translateX(0)' : 'translateX(-20px)',
              transition: 'opacity 0.35s ease, transform 0.35s ease',
            }}
          >
            <span style={{
              color: accentColor,
              fontSize: '1.4vw',
              lineHeight: 1.5,
              flexShrink: 0,
            }}>▶</span>
            <span style={{
              fontSize: '1.55vw',
              fontWeight: isActive ? 700 : 500,
              color: '#1e293b',
              lineHeight: 1.5,
            }}>
              {text}
            </span>
          </div>
        );
      })}
    </div>
  );
}

// ── step map ─────────────────────────────────────────────────────────────────
// step 0  : nothing visible
// step 1  : Fáze 1 title
// step 2-4: Fáze 1 bullets
// step 5  : Fáze 2 title
// step 6-9: Fáze 2 bullets
export const MAX_PHASE_STEP = 9;

interface Props {
  step: number;
}

export default function PhaseSlide({ step }: Props) {
  // Progress dots
  const totalDots = MAX_PHASE_STEP;
  const dots = Array.from({ length: totalDots }, (_, i) => i + 1);

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: '#f1f5f9',
      padding: '2.5vw 4vw',
      gap: '2vh',
      boxSizing: 'border-box',
      boxShadow: '0 40px 120px rgba(0,0,0,0.8), 0 0 0 3px #334155',
      overflow: 'hidden',
      fontFamily: "'Segoe UI', sans-serif",
    }}>
      {/* Slide title */}
      <h1 style={{
        textAlign: 'center',
        fontSize: '3vw',
        fontWeight: 900,
        color: '#0f172a',
        letterSpacing: '-0.02em',
        margin: 0,
      }}>
        Instrukční cyklus CPU
      </h1>

      {/* Two phase panels */}
      <div style={{ flex: 1, display: 'flex', gap: '3vw', minHeight: 0 }}>
        <PhasePanel
          title="Fáze 1 — Načtení"
          titleStep={1}
          bullets={[
            'Čítač programu ukazuje na adresu instrukce',
            'Instrukce načtena do registru instrukce',
            'Čítač programu se zvýší o 1 (výjimka: skoky)',
          ]}
          bulletSteps={[2, 3, 4]}
          step={step}
          accentColor="#1d4ed8"
          bgColor="#dbeafe"
          borderColor="#93c5fd"
        />
        <PhasePanel
          title="Fáze 2 — Provedení"
          titleStep={5}
          bullets={[
            'Identifikace operace a operandů',
            'ALU provede operaci',
            'Výsledek zapsán do registru Rd',
            'Aktualizace příznaků SREG',
          ]}
          bulletSteps={[6, 7, 8, 9]}
          step={step}
          accentColor="#7c3aed"
          bgColor="#ede9fe"
          borderColor="#c4b5fd"
        />
      </div>

      {/* Navigation bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '1.2vw',
        color: '#94a3b8',
        fontSize: '1.1vw',
        userSelect: 'none',
      }}>
        <span style={{ fontSize: '1.3vw' }}>←</span>

        {/* Progress dots */}
        <div style={{ display: 'flex', gap: '0.4vw', alignItems: 'center' }}>
          {dots.map(d => (
            <div
              key={d}
              style={{
                width: '0.55vw',
                height: '0.55vw',
                borderRadius: '50%',
                backgroundColor: step >= d ? (d <= 4 ? '#1d4ed8' : '#7c3aed') : '#cbd5e1',
                transition: 'background-color 0.3s ease',
              }}
            />
          ))}
        </div>

        <span style={{ fontSize: '1.3vw' }}>→</span>
      </div>
    </div>
  );
}
