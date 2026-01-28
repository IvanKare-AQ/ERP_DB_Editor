import React from 'react'
import './Toolbar.css'

function Toolbar({ 
  onSave, 
  onExport, 
  onColumnVisibility, 
  onSaveView, 
  onFilter, 
  onToggleView, 
  onCommitItems,
  saveEnabled = false,
  saveViewEnabled = false,
  currentView = 'primary'
}) {
  return (
    <div className="toolbar">
      <div className="toolbar-section">
        <button 
          className="toolbar-btn" 
          onClick={onSave}
          disabled={!saveEnabled}
        >
          Save
        </button>
        <button 
          className="toolbar-btn toolbar-btn-with-icon" 
          onClick={onExport}
        >
          <span className="toolbar-btn-icon">⬇</span>
          Excel
        </button>
      </div>
      
      <div className="toolbar-separator"></div>
      
      <div className="toolbar-section">
        <button 
          className="toolbar-btn" 
          onClick={onColumnVisibility}
        >
          Column Visibility
        </button>
        <button 
          className="toolbar-btn" 
          onClick={onSaveView}
          disabled={!saveViewEnabled}
        >
          Save View
        </button>
      </div>
      
      <div className="toolbar-separator"></div>
      
      <div className="toolbar-section">
        <button 
          className="toolbar-btn" 
          onClick={onFilter}
        >
          Filter Data
        </button>
        <button 
          className="toolbar-btn" 
          onClick={onToggleView}
        >
          {currentView === 'primary' ? 'Show New Items' : 'Show Current Items'}
        </button>
        <button 
          className="toolbar-btn" 
          onClick={onCommitItems}
        >
          Commit Items
        </button>
      </div>
    </div>
  )
}

export default Toolbar
