import { Check, ChevronDown, ChevronUp } from 'lucide-react';
import { PersonaGroup } from '../data/personaGroups';

interface FieldGroupProps {
  groupKey: string;
  group: PersonaGroup;
  selectedFields: Record<string, boolean>;
  expandedGroups: Record<string, boolean>;
  onToggleGroup: (groupKey: string) => void;
  onToggleField: (fieldId: string) => void;
  onToggleExpansion: (groupKey: string) => void;
}

export const FieldGroup = ({
  groupKey,
  group,
  selectedFields,
  expandedGroups,
  onToggleGroup,
  onToggleField,
  onToggleExpansion,
}: FieldGroupProps) => {
  const allSelected = group.fields.every(field => selectedFields[field.id]);
  const someSelected = group.fields.some(field => selectedFields[field.id]);
  const isExpanded = expandedGroups[groupKey];

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <div className="bg-gray-50 p-4 flex items-center justify-between">
        <div className="flex items-center gap-3 flex-1">
          <button
            onClick={() => onToggleGroup(groupKey)}
            className={`w-6 h-6 rounded border-2 flex items-center justify-center transition-colors ${
              allSelected
                ? 'bg-indigo-600 border-indigo-600'
                : someSelected
                ? 'bg-indigo-300 border-indigo-300'
                : 'border-gray-300 bg-white'
            }`}
          >
            {allSelected && <Check size={16} className="text-white" />}
          </button>
          <h3 className="font-semibold text-gray-800">
            Group {groupKey}: {group.name}
          </h3>
          <span className="text-sm text-gray-500">
            ({group.fields.filter(f => selectedFields[f.id]).length}/{group.fields.length} selected)
          </span>
        </div>
        <button
          onClick={() => onToggleExpansion(groupKey)}
          className="text-gray-500 hover:text-gray-700"
        >
          {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      {isExpanded && (
        <div className="p-4 space-y-2">
          {group.fields.map(field => (
            <div
              key={field.id}
              onClick={() => onToggleField(field.id)}
              className={`flex items-start gap-3 p-3 rounded-lg cursor-pointer transition-colors ${
                selectedFields[field.id]
                  ? 'bg-indigo-50 hover:bg-indigo-100'
                  : 'bg-white hover:bg-gray-50'
              }`}
            >
              <div
                className={`w-5 h-5 rounded border-2 flex items-center justify-center mt-0.5 flex-shrink-0 ${
                  selectedFields[field.id]
                    ? 'bg-indigo-600 border-indigo-600'
                    : 'border-gray-300 bg-white'
                }`}
              >
                {selectedFields[field.id] && <Check size={14} className="text-white" />}
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-800">{field.label}</p>
                <p className="text-sm text-gray-600 mt-1">{field.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

