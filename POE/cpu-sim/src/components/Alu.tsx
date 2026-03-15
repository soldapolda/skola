export default function Alu() {
  return (
    <div className="flex-1 flex justify-center items-center">
      <div
        className="flex items-center justify-center shadow-2xl"
        style={{
          width: '28vw',
          height: '22vh',
          backgroundColor: '#d9e2d5',
          border: '6px solid #000',
          clipPath: 'polygon(0% 0%, 100% 0%, 75% 100%, 25% 100%)',
        }}
      >
        <span className="font-black tracking-tighter" style={{ fontSize: '7vw' }}>
          ALU
        </span>
      </div>
    </div>
  );
}
