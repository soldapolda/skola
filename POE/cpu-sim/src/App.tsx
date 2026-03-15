import { initialState } from './data';
import CpuSlide from './components/CpuSlide';

export default function App() {
  return <CpuSlide state={initialState} />;
}
