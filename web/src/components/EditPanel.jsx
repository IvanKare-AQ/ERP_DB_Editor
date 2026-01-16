import React, { useState } from 'react'
import ManualEditor from './ManualEditor'
import AIEditor from './AIEditor'
import MLEditor from './MLEditor'
import './EditPanel.css'

function EditPanel({ selectedItem, onItemUpdate, onClearSelection }) {
  const [activeTab, setActiveTab] = useState('editor')

  return (
    <div className="edit-panel">
      <div className="edit-panel-tabs">
        <button
          className={`edit-tab ${activeTab === 'editor' ? 'active' : ''}`}
          onClick={() => setActiveTab('editor')}
        >
          Editor ✏️
        </button>
        <button
          className={`edit-tab ${activeTab === 'ai' ? 'active' : ''}`}
          onClick={() => setActiveTab('ai')}
        >
          AI 🤖
        </button>
        <button
          className={`edit-tab ${activeTab === 'ml' ? 'active' : ''}`}
          onClick={() => setActiveTab('ml')}
        >
          ML 🧠
        </button>
      </div>
      
      <div className="edit-panel-content">
        {activeTab === 'editor' && (
          <ManualEditor 
            selectedItem={selectedItem} 
            onItemUpdate={onItemUpdate}
            onClearSelection={onClearSelection}
          />
        )}
        {activeTab === 'ai' && (
          <AIEditor 
            selectedItem={selectedItem} 
            onItemUpdate={onItemUpdate}
          />
        )}
        {activeTab === 'ml' && (
          <MLEditor 
            selectedItem={selectedItem} 
            onItemUpdate={onItemUpdate}
          />
        )}
      </div>
    </div>
  )
}

export default EditPanel
