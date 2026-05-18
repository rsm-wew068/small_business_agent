const ACTIONS = [
  "What services do you offer?",
  "I need an oil change",
  "Book an appointment",
  "What are your hours?",
]

export default function QuickActions({ onSelect }) {
  return (
    <div className="px-4 pb-3">
      <div className="flex flex-wrap gap-2 justify-center max-w-3xl mx-auto">
        {ACTIONS.map((action) => (
          <button
            key={action}
            onClick={() => onSelect(action)}
            className="text-sm px-4 py-2 rounded-full border border-gray-200 bg-white text-gray-700 hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-700 transition-colors shadow-sm"
          >
            {action}
          </button>
        ))}
      </div>
    </div>
  )
}
