import { useState } from 'react';
import { Download, ChevronLeft, ChevronRight } from 'lucide-react';

interface PersonalityTestProps {
  onClose: () => void;
  onComplete?: (testData: any) => void;
}

const questions = [
  "Am the life of the party.",
  "Feel little concern for others.",
  "Am always prepared.",
  "Get stressed out easily.",
  "Have a rich vocabulary.",
  "Don't talk a lot.",
  "Am interested in people.",
  "Leave my belongings around.",
  "Am relaxed most of the time.",
  "Have difficulty understanding abstract ideas.",
  "Feel comfortable around people.",
  "Insult people.",
  "Pay attention to details.",
  "Worry about things.",
  "Have a vivid imagination.",
  "Keep in the background.",
  "Sympathize with others' feelings.",
  "Make a mess of things.",
  "Seldom feel blue.",
  "Am not interested in abstract ideas.",
  "Start conversations.",
  "Am not interested in other people's problems.",
  "Get chores done right away.",
  "Am easily disturbed.",
  "Have excellent ideas.",
  "Have little to say.",
  "Have a soft heart.",
  "Often forget to put things back in their proper place.",
  "Get upset easily.",
  "Do not have a good imagination.",
  "Talk to a lot of different people at parties.",
  "Am not really interested in others.",
  "Like order.",
  "Change my mood a lot.",
  "Am quick to understand things.",
  "Don't like to draw attention to myself.",
  "Take time out for others.",
  "Shirk my duties.",
  "Have frequent mood swings.",
  "Use difficult words.",
  "Don't mind being the center of attention.",
  "Feel others' emotions.",
  "Follow a schedule.",
  "Get irritated easily.",
  "Spend time reflecting on things.",
  "Am quiet around strangers.",
  "Make people feel at ease.",
  "Am exacting in my work.",
  "Often feel blue.",
  "Am full of ideas.",
];

const scaleLabels = [
  { value: 1, label: "Disagree" },
  { value: 2, label: "Slightly disagree" },
  { value: 3, label: "Neutral" },
  { value: 4, label: "Slightly agree" },
  { value: 5, label: "Agree" },
];

export const PersonalityTest = ({ onClose, onComplete }: PersonalityTestProps) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [isComplete, setIsComplete] = useState(false);

  const handleAnswer = (value: number) => {
    const newAnswers = { ...answers, [currentQuestion]: value };
    setAnswers(newAnswers);

    // Check if all questions are answered
    if (Object.keys(newAnswers).length === questions.length) {
      setIsComplete(true);
    }
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const getTestResults = () => {
    return questions.map((question, index) => ({
      questionNumber: index + 1,
      question: question,
      answer: answers[index] || null,
      answerLabel: answers[index] ? scaleLabels[answers[index] - 1].label : "Not answered",
    }));
  };

  const handleDownload = () => {
    const results = getTestResults();
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `personality-test-responses-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    // Notify parent that test is complete
    if (onComplete) {
      onComplete(results);
    }
  };

  const progress = ((Object.keys(answers).length / questions.length) * 100).toFixed(0);

  if (isComplete) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-2xl p-8 border border-gray-100">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Test Complete!</h2>
            <p className="text-gray-600">You have answered all 50 questions. You can now download your responses.</p>
          </div>

          <div className="bg-gray-50 border border-gray-300 rounded-lg p-4 mb-6">
            <p className="text-sm text-gray-700">
              <strong>Note:</strong> If you don't have time to complete the persona background right now, you can download your responses at any time to avoid losing your progress.
            </p>
          </div>

          <div className="flex flex-col items-center gap-4">
            <div className="flex gap-3">
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 bg-white text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors font-medium border border-gray-300"
              >
                <Download size={20} />
                Download Responses
              </button>
              <button
                onClick={() => {
                  const results = getTestResults();
                  if (onComplete) {
                    onComplete(results);
                  }
                  onClose();
                }}
                className="flex items-center gap-2 bg-gray-900 text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition-colors font-medium"
              >
                Send & Complete
              </button>
            </div>
            <button
              onClick={onClose}
              className="text-gray-600 hover:text-gray-800 underline text-sm"
            >
              Back to Main
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-2xl p-8 border border-gray-100">
        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <span className="text-sm font-medium text-gray-700">
              {progress}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-gray-700 h-3 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Question */}
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">
            {questions[currentQuestion]}
          </h2>

          {/* Answer Scale */}
          <div className="space-y-3">
            {scaleLabels.map((scale) => (
              <button
                key={scale.value}
                onClick={() => handleAnswer(scale.value)}
                className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
                  answers[currentQuestion] === scale.value
                    ? 'border-gray-900 bg-gray-100 text-gray-900 font-medium'
                    : 'border-gray-300 bg-white hover:border-gray-400 hover:bg-gray-50 text-gray-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-lg">{scale.label}</span>
                  <span className="text-gray-500">{scale.value}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center pt-6 border-t border-gray-300">
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-colors font-medium ${
              currentQuestion === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
            }`}
          >
            <ChevronLeft size={20} />
            Previous
          </button>

          <div className="text-sm text-gray-500">
            {answers[currentQuestion] ? `Selected: ${scaleLabels[answers[currentQuestion] - 1].label}` : 'Please select an answer'}
          </div>

          <button
            onClick={handleNext}
            disabled={currentQuestion === questions.length - 1 || !answers[currentQuestion]}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-colors font-medium ${
              currentQuestion === questions.length - 1 || !answers[currentQuestion]
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-900 text-white hover:bg-gray-800'
            }`}
          >
            Next
            <ChevronRight size={20} />
          </button>
        </div>

        {/* Close Button */}
        <div className="mt-6 text-center">
          <button
            onClick={onClose}
            className="text-gray-600 hover:text-gray-800 underline text-sm"
          >
            Cancel Test
          </button>
        </div>
      </div>
    </div>
  );
};

