import { Download, Send } from 'lucide-react';
import { FormField } from './FormField';
import { personaGroups } from '../data/personaGroups';

interface PersonaFormProps {
  selectedFields: Record<string, boolean>;
  formData: Record<string, string>;
  onInputChange: (fieldId: string, value: string) => void;
  onExportJSON: () => void;
  onExportXML: () => void;
  onExportText: () => void;
  onSend?: () => void;
}

export const PersonaForm = ({
  selectedFields,
  formData,
  onInputChange,
  onExportJSON,
  onExportXML,
  onExportText,
  onSend,
}: PersonaFormProps) => {
  return (
    <div className="space-y-6">
      <div className="bg-gray-50 border border-gray-300 rounded-lg p-4 mb-6">
        <p className="text-gray-700 text-sm">
          Fill in the selected persona attributes. Only the fields you selected in the previous step are shown here.
        </p>
      </div>

      {Object.entries(personaGroups).map(([groupKey, group]) => {
        const selectedGroupFields = group.fields.filter(field => selectedFields[field.id]);

        if (selectedGroupFields.length === 0) return null;

        return (
          <div key={groupKey} className="bg-white border border-gray-300 rounded-lg p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              Group {groupKey}: {group.name}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {selectedGroupFields.map(field => (
                <FormField
                  key={field.id}
                  field={field}
                  value={formData[field.id] || ''}
                  onChange={(value) => onInputChange(field.id, value)}
                />
              ))}
            </div>
          </div>
        );
      })}

      {/* Send Button */}
      {onSend && (
        <div className="pt-6 border-t border-gray-300 mb-4">
          <div className="bg-gray-50 border border-gray-300 rounded-lg p-4 mb-4">
            <p className="text-sm text-gray-700">
              <strong>Note:</strong> If you don't have time to complete the personality test right now, you can download your responses at any time to avoid losing your progress.
            </p>
          </div>
          <div className="flex justify-center">
            <button
              onClick={onSend}
              className="flex items-center gap-2 bg-gray-900 text-white px-8 py-4 rounded-lg hover:bg-gray-800 transition-colors font-medium text-lg shadow-lg"
            >
              <Send size={20} />
              Send Persona Background
            </button>
          </div>
        </div>
      )}

      {/* Export Buttons */}
      <div className="flex gap-3 justify-center pt-4 border-t border-gray-300">
        <p className="text-sm text-gray-600 mr-4 self-center">Or download individually:</p>
        <button
          onClick={onExportJSON}
          className="flex items-center gap-2 bg-white text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors font-medium text-sm border border-gray-300"
        >
          <Download size={16} />
          JSON
        </button>
        <button
          onClick={onExportXML}
          className="flex items-center gap-2 bg-gray-50 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors font-medium text-sm border border-gray-300"
        >
          <Download size={16} />
          XML
        </button>
        <button
          onClick={onExportText}
          className="flex items-center gap-2 bg-white text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors font-medium text-sm border border-gray-300"
        >
          <Download size={16} />
          Text
        </button>
      </div>
    </div>
  );
};

