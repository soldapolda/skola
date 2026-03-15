import type { DecodedInstruction } from '../types';

interface Props {
  decoded: DecodedInstruction;
}

export default function Dekodovani({ decoded }: Props) {
  return (
    <div
      className="shadow-2xl rounded-lg"
      style={{
        width: '21vw',
        padding: '0.9vw',
        backgroundColor: '#c48e8e',
        border: '4px solid #333',
      }}
    >
      <h3
        className="text-center font-black uppercase border-b-4 border-black/10"
        style={{ fontSize: '1.5vw', marginBottom: '1vh', paddingBottom: '0.5vh' }}
      >
        Dekodování
      </h3>
      <div
        className="font-mono font-black text-center text-white rounded"
        style={{ backgroundColor: '#1d4ed8', fontSize: '1.8vw', padding: '0.8vh 0' }}
      >
        {decoded.raw}
      </div>
    </div>
  );
}
