import { Code } from 'lucide-react';

interface HeaderProps {
  showPrompt: boolean;
  onTogglePrompt: () => void;
}

export const Header = ({ showPrompt, onTogglePrompt }: HeaderProps) => {
  return (
    <div className="bg-blue-600 border-b border-blue-700 p-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Persona Pattern Builder</h1>
          <p className="text-blue-100 mt-2">Design comprehensive user personas with customizable attributes</p>
        </div>
        <button
          onClick={onTogglePrompt}
          className="flex items-center gap-2 bg-white text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-50 transition-colors border border-blue-300"
        >
          <Code size={20} />
          {showPrompt ? 'Back to Builder' : 'Enhancement Scripts'}
        </button>
      </div>
    </div>
  );
};

