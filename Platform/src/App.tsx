import { useState } from 'react';
import { Header } from './components/Header';
import { ScriptsPage } from './components/ScriptsPage';
import { DownloadNotification } from './components/DownloadNotification';
import { PersonalityTest } from './components/PersonalityTest';
import { Tabs } from './components/Tabs';
import { FieldSelector } from './components/FieldSelector';
import { PersonaForm } from './components/PersonaForm';
import { personaGroups } from './data/personaGroups';
import { exportJSON, exportXML, exportText } from './utils/exportUtils';
import { ArrowRight, User, Brain, ArrowLeft, FolderDown, CheckCircle } from 'lucide-react';
import JSZip from 'jszip';

type PageView = 'main' | 'persona' | 'test' | 'scripts';

function App() {
  const [currentView, setCurrentView] = useState<PageView>('main');
  const [activeTab, setActiveTab] = useState('select');
  const [showDownloadNotification, setShowDownloadNotification] = useState(false);
  const [expandedGroups, setExpandedGroups] = useState<Record<string, boolean>>({});
  
  // Completion tracking
  const [personaCompleted, setPersonaCompleted] = useState(false);
  const [personalityTestCompleted, setPersonalityTestCompleted] = useState(false);
  const [personalityTestData, setPersonalityTestData] = useState<any>(null);

  const [selectedFields, setSelectedFields] = useState<Record<string, boolean>>(() => {
    // Default set of fields that should start as selected
    const defaultSelected = new Set<string>([
      'fullName',                // Full Real Name
      'pronouns',                // Pronouns
      'preferredName',           // Preferred Name
      'age',                     // Age
      'genderIdentity',          // Gender Identity
      'ethnicity',               // Ethnicity and Cultural Background
      'nationality',             // Nationality
      'primaryLanguages',        // Primary Language(s)
      'secondaryLanguage',       // Secondary Working Language
      'primaryHobbies',          // Primary Hobbies
      'educationLevel',          // Education Level
      'fieldOfStudy',            // Field of Study
      'currentJob',              // Current Job
      'roleAuthority',           // Workplace Role Authority
      'workExperience',          // Years of Work Experience
      'industrySector',          // Industry Sector
      'digitalLiteracy',         // Digital Literacy Level
      'securityPractices',       // Security & Privacy Practices
      'trustPropensity',         // Trust Propensity
      'professionalSkills',      // Professional & Technical Skills
      'softSkills',              // Soft Skills
    ]);

    const initial: Record<string, boolean> = {};

    Object.keys(personaGroups).forEach(groupKey => {
      personaGroups[groupKey].fields.forEach(field => {
        initial[field.id] = defaultSelected.has(field.id);
      });
    });

    return initial;
  });

  const [formData, setFormData] = useState<Record<string, string>>({});

  const toggleField = (fieldId: string) => {
    setSelectedFields(prev => ({
      ...prev,
      [fieldId]: !prev[fieldId]
    }));
  };

  const toggleGroup = (groupKey: string) => {
    const allSelected = personaGroups[groupKey].fields.every(field => selectedFields[field.id]);
    const newValue = !allSelected;

    const updates: Record<string, boolean> = {};
    personaGroups[groupKey].fields.forEach(field => {
      updates[field.id] = newValue;
    });

    setSelectedFields(prev => ({
      ...prev,
      ...updates
    }));
  };

  const toggleGroupExpansion = (groupKey: string) => {
    setExpandedGroups(prev => ({
      ...prev,
      [groupKey]: !prev[groupKey]
    }));
  };

  const handleInputChange = (fieldId: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [fieldId]: value
    }));
  };

  const handleExportJSON = () => {
    exportJSON(selectedFields, formData, () => {
      setShowDownloadNotification(true);
    });
  };

  const handleExportXML = () => {
    exportXML(selectedFields, formData, () => {
      setShowDownloadNotification(true);
    });
  };

  const handleExportText = () => {
    exportText(selectedFields, formData, () => {
      setShowDownloadNotification(true);
    });
  };

  const handlePersonaSend = () => {
    setPersonaCompleted(true);
    setShowDownloadNotification(true);
  };

  const handlePersonalityTestComplete = (testData: any) => {
    setPersonalityTestCompleted(true);
    setPersonalityTestData(testData);
  };

  const handleDownloadAll = async () => {
    if (!personaCompleted || !personalityTestCompleted) return;

    const zip = new JSZip();

    // Add persona background JSON
    const personaData: Record<string, string> = {};
    Object.keys(selectedFields).forEach(fieldId => {
      if (selectedFields[fieldId] && formData[fieldId]) {
        personaData[fieldId] = formData[fieldId];
      }
    });
    zip.file('persona-background.json', JSON.stringify(personaData, null, 2));

    // Add personality test JSON
    if (personalityTestData) {
      zip.file('personality-test-responses.json', JSON.stringify(personalityTestData, null, 2));
    }

    // Generate and download zip
    const blob = await zip.generateAsync({ type: 'blob' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `persona-complete-${new Date().toISOString().split('T')[0]}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Main Landing Page
  if (currentView === 'main') {
    return (
      <div className="min-h-screen bg-landscape p-6">
        <div className="max-w-5xl mx-auto">
          <div className="bg-white rounded-lg shadow-2xl overflow-hidden border border-gray-100">
            <div className="bg-blue-600 border-b border-blue-700 p-8 text-center">
              <h1 className="text-4xl font-bold mb-3 text-white">Persona Builder</h1>
              <p className="text-blue-100 text-lg">Create comprehensive user personas with customizable attributes</p>
            </div>

            <div className="p-8">
              {/* Explanation */}
              <div className="bg-gray-50 border border-gray-200 p-6 mb-8 rounded-lg">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">Getting Started</h2>
                <p className="text-gray-700 leading-relaxed">
                  To create your complete persona, you need to complete <strong>both</strong> steps below:
                </p>
                <ul className="mt-4 space-y-2 text-gray-700">
                  <li className="flex items-start">
                    <span className="text-gray-600 font-semibold mr-2">1.</span>
                    <span><strong>Create Persona Background</strong> - Select and fill in persona attributes and characteristics</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-gray-600 font-semibold mr-2">2.</span>
                    <span><strong>Do Personality Test</strong> - Complete the personality assessment to get detailed personality insights</span>
                  </li>
                </ul>
                <p className="mt-4 text-gray-700">
                  After completing both steps and downloading your responses, send us all the information and we will create your persona.
                </p>
              </div>

              {/* Cards */}
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                {/* Create Persona Background Card */}
                <button
                  onClick={() => setCurrentView('persona')}
                  className={`group bg-white border-2 rounded-xl p-8 hover:shadow-2xl transition-all text-left relative ${
                    personaCompleted 
                      ? 'border-green-500 hover:border-green-600' 
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  {personaCompleted && (
                    <div className="absolute top-4 right-4">
                      <CheckCircle size={24} className="text-green-600" />
                    </div>
                  )}
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-gray-100 p-4 rounded-lg">
                      <User size={32} className="text-gray-700" />
                    </div>
                    <ArrowRight size={24} className="text-gray-400 group-hover:text-gray-700 group-hover:translate-x-1 transition-all" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">Create Persona Background</h3>
                  <p className="text-gray-600 leading-relaxed">
                    Select persona attributes and fill in detailed information about demographics, background, goals, and characteristics.
                  </p>
                  {personaCompleted && (
                    <div className="mt-4 text-sm text-green-600 font-medium">
                      ✓ Completed
                    </div>
                  )}
                </button>

                {/* Do Personality Test Card */}
                <button
                  onClick={() => setCurrentView('test')}
                  className={`group bg-gray-50 border-2 rounded-xl p-8 hover:shadow-2xl transition-all text-left relative ${
                    personalityTestCompleted 
                      ? 'border-green-500 hover:border-green-600' 
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  {personalityTestCompleted && (
                    <div className="absolute top-4 right-4">
                      <CheckCircle size={24} className="text-green-600" />
                    </div>
                  )}
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-gray-200 p-4 rounded-lg">
                      <Brain size={32} className="text-gray-700" />
                    </div>
                    <ArrowRight size={24} className="text-gray-400 group-hover:text-gray-700 group-hover:translate-x-1 transition-all" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">Do Personality Test</h3>
                  <p className="text-gray-600 leading-relaxed">
                    Complete a comprehensive personality assessment to understand behavioral patterns, traits, and psychological characteristics.
                  </p>
                  {personalityTestCompleted && (
                    <div className="mt-4 text-sm text-green-600 font-medium">
                      ✓ Completed
                    </div>
                  )}
                </button>
              </div>

              {/* Download All Section */}
              {personaCompleted && personalityTestCompleted ? (
                <div className="bg-white border-2 border-gray-300 rounded-xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 mb-2">All Assignments Complete!</h3>
                      <p className="text-gray-700">
                        You have completed both assignments. Download a folder containing all your persona documents.
                      </p>
                    </div>
                    <button
                      onClick={handleDownloadAll}
                      className="flex items-center gap-2 bg-gray-900 text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition-colors font-medium text-lg shadow-lg"
                    >
                      <FolderDown size={24} />
                      Download All Documents
                    </button>
                  </div>
                </div>
              ) : (
                <div className="bg-gray-50 border border-gray-300 p-4 rounded-lg">
                  <p className="text-gray-700 text-sm">
                    <strong>Note:</strong> Complete both assignments above to download a folder containing all your persona documents (persona background and personality test responses). Individual downloads are still available on each page.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Scripts Page
  if (currentView === 'scripts') {
    return (
      <div className="min-h-screen bg-landscape p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-lg shadow-2xl overflow-hidden border border-gray-100">
            <Header showPrompt={true} onTogglePrompt={() => setCurrentView('main')} />
            <ScriptsPage onBack={() => setCurrentView('main')} />
          </div>
        </div>
      </div>
    );
  }

  // Personality Test Page
  if (currentView === 'test') {
    return (
      <div className="min-h-screen bg-landscape p-6">
        <div className="max-w-7xl mx-auto">
          <div className="mb-4">
            <button
              onClick={() => setCurrentView('main')}
              className="flex items-center gap-2 bg-white text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors font-medium border border-gray-300 shadow-sm"
            >
              <ArrowLeft size={20} />
              <span>Back to Main</span>
            </button>
          </div>
          <PersonalityTest 
            onClose={() => setCurrentView('main')} 
            onComplete={handlePersonalityTestComplete}
          />
        </div>
      </div>
    );
  }

  // Persona Creation Page
  if (currentView === 'persona') {
    return (
      <div className="min-h-screen bg-landscape p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-lg shadow-2xl overflow-hidden border border-gray-100">
            <div className="bg-blue-600 border-b border-blue-700 p-6">
              <div className="flex justify-between items-center">
                <div>
                  <h1 className="text-3xl font-bold text-white">Create Persona Background</h1>
                  <p className="text-blue-100 mt-2">Select attributes and fill in persona details</p>
                </div>
                <button
                  onClick={() => setCurrentView('main')}
                  className="flex items-center gap-2 bg-white text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-50 transition-colors font-medium border border-blue-300"
                >
                  <ArrowLeft size={20} />
                  Back to Main
                </button>
              </div>
            </div>

            <Tabs activeTab={activeTab} onTabChange={setActiveTab} />

            <div className="p-6">
              {activeTab === 'select' && (
                <FieldSelector
                  selectedFields={selectedFields}
                  expandedGroups={expandedGroups}
                  onToggleGroup={toggleGroup}
                  onToggleField={toggleField}
                  onToggleExpansion={toggleGroupExpansion}
                />
              )}

              {activeTab === 'form' && (
                <PersonaForm
                  selectedFields={selectedFields}
                  formData={formData}
                  onInputChange={handleInputChange}
                  onExportJSON={handleExportJSON}
                  onExportXML={handleExportXML}
                  onExportText={handleExportText}
                  onSend={handlePersonaSend}
                />
              )}
            </div>
          </div>
        </div>

        {showDownloadNotification && (
          <DownloadNotification
            onClose={() => setShowDownloadNotification(false)}
          />
        )}
      </div>
    );
  }

  return null;
}

export default App;

