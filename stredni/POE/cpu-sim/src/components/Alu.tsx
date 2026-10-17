interface Props {
  active?: boolean;
}

export default function Alu({ active = false }: Props) {
  return (
    <div className="flex-1 flex justify-center items-center">
      <div
        id="alu-shape"
        className="flex items-center justify-center shadow-2xl"
        style={{
          width: '28vw',
          height: '22vh',
          backgroundColor: active ? '#fef9c3' : '#d9e2d5',
          border: active ? '6px solid #f59e0b' : '6px solid #000',
          clipPath: 'polygon(0% 0%, 100% 0%, 75% 100%, 25% 100%)',
          // drop-shadow respects clip-path, box-shadow does not
          filter: active ? 'drop-shadow(0 0 10px #f59e0b)' : undefined,
          transition: 'background-color 0.3s, border-color 0.3s, filter 0.3s',
        }}
      >
        <span
          className="font-black tracking-tighter"
          style={{ fontSize: '7vw', color: active ? '#b45309' : '#000' }}
        >
          ALU
        </span>
      </div>
    </div>
  );
}
