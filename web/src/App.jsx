import { useState } from 'react'
import ErrorBoundary from './components/ErrorBoundary'
import Toolbar from './components/Toolbar'
import TreeView from './components/TreeView'
import EditPanel from './components/EditPanel'
import './App.css'

function App() {
  const [selectedItem, setSelectedItem] = useState(null)
  const [selectedItemId, setSelectedItemId] = useState(null)
  const [currentView, setCurrentView] = useState('primary')
  const [dataChanged, setDataChanged] = useState(false)
  const [viewChanged, setViewChanged] = useState(false)

  const handleItemSelect = (item, itemId) => {
    setSelectedItem(item)
    setSelectedItemId(itemId)
  }

  const handleItemUpdate = () => {
    setDataChanged(true)
    // Reload tree view or refresh data
  }

  const handleSave = async () => {
    // TODO: Implement save functionality
    console.log('Save clicked')
    setDataChanged(false)
  }

  const handleExport = () => {
    // TODO: Implement export functionality
    console.log('Export clicked')
  }

  const handleColumnVisibility = () => {
    // TODO: Implement column visibility dialog
    console.log('Column Visibility clicked')
  }

  const handleSaveView = () => {
    // TODO: Implement save view functionality
    console.log('Save View clicked')
    setViewChanged(false)
  }

  const handleFilter = () => {
    // TODO: Implement filter dialog
    console.log('Filter clicked')
  }

  const handleToggleView = () => {
    setCurrentView(currentView === 'primary' ? 'added' : 'primary')
  }

  const handleCommitItems = async () => {
    // TODO: Implement commit items functionality
    console.log('Commit Items clicked')
  }

  return (
    <ErrorBoundary>
      <div className="App">
        <div className="app-header">
          <h1>ERP Database Editor</h1>
        </div>
        
        <Toolbar
          onSave={handleSave}
          onExport={handleExport}
          onColumnVisibility={handleColumnVisibility}
          onSaveView={handleSaveView}
          onFilter={handleFilter}
          onToggleView={handleToggleView}
          onCommitItems={handleCommitItems}
          saveEnabled={dataChanged}
          saveViewEnabled={viewChanged}
          currentView={currentView}
        />
        
        <div className="app-content">
          <div className="app-left-panel">
            <ErrorBoundary>
              <TreeView
                onItemSelect={handleItemSelect}
                selectedItemId={selectedItemId}
              />
            </ErrorBoundary>
          </div>
          
        <div className="app-right-panel">
          <ErrorBoundary>
            <EditPanel
              selectedItem={selectedItem}
              onItemUpdate={handleItemUpdate}
              onClearSelection={() => {
                setSelectedItem(null)
                setSelectedItemId(null)
              }}
            />
          </ErrorBoundary>
        </div>
        </div>
      </div>
    </ErrorBoundary>
  )
}

export default App
