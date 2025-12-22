import { X, CheckCircle } from 'lucide-react';

interface DownloadNotificationProps {
  onClose: () => void;
}

export const DownloadNotification = ({ onClose }: DownloadNotificationProps) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl max-w-md w-full p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X size={24} />
        </button>
        
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-green-100 rounded-full p-2">
            <CheckCircle className="text-green-600" size={32} />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-800">Thank You!</h3>
            <p className="text-sm text-gray-600">Your persona background has been saved</p>
          </div>
        </div>

        <div className="bg-blue-50 border-l-4 border-blue-500 rounded-r-lg p-4 mb-4">
          <p className="text-sm text-gray-700">
            <strong>Note:</strong> If you don't have time to complete the personality test right now, you can download your responses at any time to avoid losing your progress.
          </p>
        </div>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

