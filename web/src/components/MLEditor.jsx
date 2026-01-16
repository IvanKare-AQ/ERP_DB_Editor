import React from 'react'
import './MLEditor.css'

function MLEditor({ selectedItem, onItemUpdate }) {
  return (
    <div className="ml-editor">
      <h2>Machine Learning</h2>
      {selectedItem ? (
        <p>ML Editor functionality coming soon...</p>
      ) : (
        <p className="no-selection">Select an item from the tree view to use ML features</p>
      )}
    </div>
  )
}

export default MLEditor
