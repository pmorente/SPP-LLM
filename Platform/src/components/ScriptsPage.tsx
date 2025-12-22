import { Copy, Check, ArrowLeft, Code, Terminal } from 'lucide-react';
import { useState } from 'react';
import { generateEnhancementScripts } from '../utils/exportUtils';

interface ScriptsPageProps {
  onBack: () => void;
}

export const ScriptsPage = ({ onBack }: ScriptsPageProps) => {
  const [copiedScript, setCopiedScript] = useState<string | null>(null);
  const scripts = generateEnhancementScripts();

  const handleCopy = (scriptKey: string, content: string) => {
    navigator.clipboard.writeText(content);
    setCopiedScript(scriptKey);
    setTimeout(() => setCopiedScript(null), 2000);
  };

  const ScriptCard = ({ title, description, content, scriptKey }: {
    title: string;
    description: string;
    content: string;
    scriptKey: string;
  }) => (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <div className="bg-gray-50 px-4 py-3 flex items-center justify-between border-b border-gray-200">
        <div className="flex items-center gap-3">
          <Terminal className="text-indigo-600" size={20} />
          <div>
            <h3 className="font-semibold text-gray-800">{title}</h3>
            <p className="text-xs text-gray-600">{description}</p>
          </div>
        </div>
        <button
          onClick={() => handleCopy(scriptKey, content)}
          className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors text-sm"
        >
          {copiedScript === scriptKey ? (
            <>
              <Check size={16} />
              Copied!
            </>
          ) : (
            <>
              <Copy size={16} />
              Copy
            </>
          )}
        </button>
      </div>
      <pre className="bg-gray-900 text-green-400 p-4 overflow-x-auto text-sm">
        <code>{content}</code>
      </pre>
    </div>
  );

  return (
    <div className="p-6">
      <div className="mb-6">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-indigo-600 hover:text-indigo-700 mb-4 transition-colors"
        >
          <ArrowLeft size={20} />
          Back to Persona Builder
        </button>
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6 border border-indigo-200">
          <div className="flex items-start gap-4">
            <div className="bg-indigo-600 rounded-lg p-3">
              <Code className="text-white" size={32} />
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Enhancement Scripts</h2>
              <p className="text-gray-600 mb-4">
                Copy these scripts to enhance your downloaded persona patterns. These scripts can analyze your persona data, 
                add computed fields, and provide deeper insights.
              </p>
              <div className="bg-white rounded-lg p-4 border border-indigo-100">
                <p className="text-sm text-gray-700">
                  <strong>Usage:</strong> After downloading your persona pattern, save one of these scripts to a file, 
                  make it executable (if needed), and run it with your persona pattern file as an argument.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <ScriptCard
          title="Python Enhancement Script"
          description="Requires Python 3.6+. Run with: python enhance_persona.py persona-pattern.json"
          content={scripts.python}
          scriptKey="python"
        />

        <ScriptCard
          title="Bash Enhancement Script"
          description="Requires bash and jq (optional). Run with: ./enhance_persona.sh persona-pattern.json"
          content={scripts.bash}
          scriptKey="bash"
        />

        <ScriptCard
          title="Node.js Enhancement Script"
          description="Requires Node.js. Run with: node enhance_persona.js persona-pattern.json"
          content={scripts.nodejs}
          scriptKey="nodejs"
        />
      </div>

      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> These scripts are examples. You can modify them to add your own enhancement logic, 
          such as calculating derived metrics, validating data, or integrating with external APIs.
        </p>
      </div>
    </div>
  );
};

