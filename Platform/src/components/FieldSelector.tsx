import { FieldGroup } from './FieldGroup';
import { personaGroups } from '../data/personaGroups';

interface FieldSelectorProps {
  selectedFields: Record<string, boolean>;
  expandedGroups: Record<string, boolean>;
  onToggleGroup: (groupKey: string) => void;
  onToggleField: (fieldId: string) => void;
  onToggleExpansion: (groupKey: string) => void;
}

export const FieldSelector = ({
  selectedFields,
  expandedGroups,
  onToggleGroup,
  onToggleField,
  onToggleExpansion,
}: FieldSelectorProps) => {
  return (
    <div className="space-y-4">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <p className="text-blue-800 text-sm">
          Select the variables you want to include in your persona. All variables are selected by default. Click on individual items or group headers to toggle selection.
        </p>
      </div>

      {Object.entries(personaGroups).map(([groupKey, group]) => (
        <FieldGroup
          key={groupKey}
          groupKey={groupKey}
          group={group}
          selectedFields={selectedFields}
          expandedGroups={expandedGroups}
          onToggleGroup={onToggleGroup}
          onToggleField={onToggleField}
          onToggleExpansion={onToggleExpansion}
        />
      ))}
    </div>
  );
};

