interface TabsProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export const Tabs = ({ activeTab, onTabChange }: TabsProps) => {
  return (
    <div className="flex border-b border-gray-300">
      <button
        onClick={() => onTabChange('select')}
        className={`flex-1 py-4 px-6 font-medium transition-colors ${
          activeTab === 'select'
            ? 'bg-white text-gray-900 border-b-2 border-gray-900'
            : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
        }`}
      >
        1. Select Variables
      </button>
      <button
        onClick={() => onTabChange('form')}
        className={`flex-1 py-4 px-6 font-medium transition-colors ${
          activeTab === 'form'
            ? 'bg-white text-gray-900 border-b-2 border-gray-900'
            : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
        }`}
      >
        2. Fill Persona Data
      </button>
    </div>
  );
};

