import React from 'react'
import './AIEditor.css'

function AIEditor({ selectedItem, onItemUpdate }) {
  return (
    <div className="ai-editor">
      <h2>AI-Powered Editing</h2>
      {selectedItem ? (
        <p>AI Editor functionality coming soon...</p>
      ) : (
        <p className="no-selection">Select an item from the tree view to use AI editing</p>
      )}
    </div>
  )
}

export default AIEditor
