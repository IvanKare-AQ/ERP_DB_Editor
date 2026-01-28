import { useState, useEffect } from 'react'
import axios from 'axios'
import ErrorBoundary from './components/ErrorBoundary'
import Toolbar from './components/Toolbar'
import TreeView from './components/TreeView'
import EditPanel from './components/EditPanel'
import ColumnVisibilityDialog from './components/ColumnVisibilityDialog'
import FilterDialog from './components/FilterDialog'
import './App.css'

function App() {
  const [selectedItem, setSelectedItem] = useState(null)
  const [selectedItemId, setSelectedItemId] = useState(null)
  const [currentView, setCurrentView] = useState('primary')
  const [dataChanged, setDataChanged] = useState(false)
  const [viewChanged, setViewChanged] = useState(false)
  const [showColumnVisibility, setShowColumnVisibility] = useState(false)
  const [showFilterDialog, setShowFilterDialog] = useState(false)
  const [allColumns, setAllColumns] = useState([])
  const [visibleColumns, setVisibleColumns] = useState([])
  const [activeFilters, setActiveFilters] = useState({})

  const handleItemSelect = (item, itemId) => {
    setSelectedItem(item)
    setSelectedItemId(itemId)
  }

  useEffect(() => {
    loadColumns()
    loadColumnVisibility()
  }, [])

  const loadColumns = async () => {
    try {
      const response = await axios.get('/api/database/columns')
      if (response.data.success) {
        setAllColumns(response.data.data || [])
        // If no visible columns set, use all columns
        if (visibleColumns.length === 0) {
          setVisibleColumns(response.data.data || [])
        }
      }
    } catch (err) {
      console.error('Error loading columns:', err)
    }
  }

  const loadColumnVisibility = async () => {
    try {
      const response = await axios.get('/api/config/column-visibility')
      if (response.data.success && response.data.visible_columns) {
        setVisibleColumns(response.data.visible_columns)
      }
    } catch (err) {
      console.error('Error loading column visibility:', err)
    }
  }

  const handleItemUpdate = () => {
    setDataChanged(true)
    // Reload tree view or refresh data
  }

  const handleSave = async () => {
    try {
      if (!confirm('Are you sure you want to save all changes to the database?')) {
        return
      }

      // Get current data from database (includes any modifications)
      const loadResponse = await axios.get('/api/database/load')
      if (!loadResponse.data.success) {
        alert('Failed to load database for saving')
        return
      }

      const saveData = {
        items: loadResponse.data.data.items
      }

      const response = await axios.post('/api/database/save', saveData)
      if (response.data.success) {
        alert('Database saved successfully')
        setDataChanged(false)
        // Reload to refresh the view
        window.location.reload()
      } else {
        alert('Failed to save database')
      }
    } catch (err) {
      console.error('Error saving database:', err)
      alert(`Failed to save database: ${err.message}`)
    }
  }

  const handleExport = async () => {
    try {
      const response = await axios.post('/api/database/export/excel', {}, {
        responseType: 'blob'
      })
      
      // Check if response is actually a blob (Excel file) or an error JSON
      if (response.data instanceof Blob) {
        // Check if it's actually an error JSON blob
        const contentType = response.headers['content-type'] || ''
        if (contentType.includes('application/json')) {
          // Error response was returned as blob, parse it
          const text = await response.data.text()
          try {
            const errorData = JSON.parse(text)
            alert(`Failed to export: ${errorData.detail || errorData.message || 'Unknown error'}`)
            return
          } catch (parseErr) {
            // If it's not parseable JSON, it might be the actual export
          }
        }
        
        // Generate filename with timestamp
        const now = new Date()
        const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, -5) // Format: YYYY-MM-DDTHH-MM-SS
        const filename = `component_database_${timestamp}.xlsx`
        
        // Create download link for Excel file
        const url = window.URL.createObjectURL(response.data)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        
        alert('Data exported to Excel successfully')
      } else {
        alert('Unexpected response format from server')
      }
    } catch (err) {
      console.error('Error exporting data:', err)
      // Try to parse error response if it's a blob
      if (err.response && err.response.data instanceof Blob) {
        try {
          const text = await err.response.data.text()
          const errorData = JSON.parse(text)
          alert(`Failed to export: ${errorData.detail || errorData.message || 'Unknown error'}`)
        } catch (parseErr) {
          alert(`Failed to export data: ${err.message}`)
        }
      } else {
        alert(`Failed to export data: ${err.message}`)
      }
    }
  }

  const handleColumnVisibility = () => {
    setShowColumnVisibility(true)
  }

  const handleColumnVisibilityApply = async (selectedColumns) => {
    try {
      setVisibleColumns(selectedColumns)
      setViewChanged(true)
      // Note: We don't save to config here - that's done by Save View button
    } catch (err) {
      console.error('Error applying column visibility:', err)
      alert(`Failed to apply column visibility: ${err.message}`)
    }
  }

  const handleSaveView = async () => {
    try {
      // Save column visibility
      await axios.post('/api/config/column-visibility', visibleColumns)
      
      // Save view settings (filters, expansion state, etc.)
      const viewSettings = {
        currentView: currentView
        // Add other view settings here as needed
      }
      await axios.post('/api/config/view-settings', viewSettings)
      
      alert('View settings saved successfully')
      setViewChanged(false)
    } catch (err) {
      console.error('Error saving view:', err)
      alert(`Failed to save view: ${err.message}`)
    }
  }

  const handleFilter = () => {
    setShowFilterDialog(true)
  }

  const handleApplyFilters = async (filters) => {
    try {
      setActiveFilters(filters)
      setViewChanged(true)
      // Note: Filtering will be applied in TreeView component
      // For now, we'll just store the filters
      setShowFilterDialog(false)
      alert('Filters applied. Note: Full filter implementation requires TreeView update.')
    } catch (err) {
      console.error('Error applying filters:', err)
      alert(`Failed to apply filters: ${err.message}`)
    }
  }

  const handleToggleView = () => {
    setCurrentView(currentView === 'primary' ? 'added' : 'primary')
    setViewChanged(true)
  }

  const handleCommitItems = async () => {
    try {
      if (!confirm('Are you sure you want to commit all draft items to the main database?')) {
        return
      }

      const response = await axios.post('/api/items/commit')
      if (response.data.success) {
        alert(response.data.message || 'Items committed successfully')
        // Reload tree view
        window.location.reload()
      } else {
        alert('Failed to commit items')
      }
    } catch (err) {
      console.error('Error committing items:', err)
      alert(`Failed to commit items: ${err.message}`)
    }
  }

  return (
    <ErrorBoundary>
      <div className="App">
        <div className="app-header">
          <h1>ERP Database Editor</h1>
          <span className="app-version">v1.5.0</span>
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
                visibleColumns={visibleColumns}
                currentView={currentView}
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

        <ColumnVisibilityDialog
          isOpen={showColumnVisibility}
          onClose={() => setShowColumnVisibility(false)}
          onApply={handleColumnVisibilityApply}
          allColumns={allColumns}
          visibleColumns={visibleColumns}
        />

        <FilterDialog
          isOpen={showFilterDialog}
          onClose={() => setShowFilterDialog(false)}
          onApply={handleApplyFilters}
          allColumns={allColumns}
        />
      </div>
    </ErrorBoundary>
  )
}

export default App
