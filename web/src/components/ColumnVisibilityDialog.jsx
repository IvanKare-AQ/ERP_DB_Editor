import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './ColumnVisibilityDialog.css'

function ColumnVisibilityDialog({ isOpen, onClose, onApply, allColumns, visibleColumns }) {
  const [columnStates, setColumnStates] = useState({})

  useEffect(() => {
    if (isOpen) {
      // Initialize column states based on current visibility
      const states = {}
      allColumns.forEach(col => {
        states[col] = visibleColumns.includes(col)
      })
      setColumnStates(states)
    }
  }, [isOpen, allColumns, visibleColumns])

  const handleToggle = (column) => {
    setColumnStates(prev => ({
      ...prev,
      [column]: !prev[column]
    }))
  }

  const handleApply = () => {
    const selectedColumns = Object.keys(columnStates).filter(col => columnStates[col])
    onApply(selectedColumns)
    onClose()
  }

  const handleCancel = () => {
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="dialog-overlay" onClick={handleCancel}>
      <div className="dialog-content column-visibility-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <h2>Column Visibility</h2>
          <button className="dialog-close" onClick={handleCancel}>×</button>
        </div>
        
        <div className="dialog-body">
          <p className="dialog-instructions">
            Select which columns should be visible in the tree view:
          </p>
          
          <div className="column-list">
            {allColumns.map(column => (
              <div key={column} className="column-checkbox-item">
                <label className="column-checkbox-label">
                  <input
                    type="checkbox"
                    checked={columnStates[column] || false}
                    onChange={() => handleToggle(column)}
                  />
                  <span>{column}</span>
                </label>
              </div>
            ))}
          </div>
        </div>
        
        <div className="dialog-footer">
          <button className="btn-apply" onClick={handleApply}>
            Apply
          </button>
          <button className="btn-cancel" onClick={handleCancel}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}

export default ColumnVisibilityDialog
