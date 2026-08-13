import { Customized, Default } from './demo';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center p-4 pt-16 gap-16">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-foreground">ProVenture App</h1>
        <p className="text-muted-foreground max-w-md">
          This is a demonstration of the mobile bottom navigation bar components.
        </p>
      </div>
      
      <div className="w-full max-w-lg flex flex-col items-center gap-6">
        <h2 className="text-xl font-semibold text-foreground border-b pb-2 w-full text-center">Customized Demo</h2>
        <Customized />
      </div>

      <div className="w-full max-w-lg flex flex-col items-center gap-6">
        <h2 className="text-xl font-semibold text-foreground border-b pb-2 w-full text-center">Default Demo</h2>
        <Default />
      </div>
    </div>
  )
}

export default App
