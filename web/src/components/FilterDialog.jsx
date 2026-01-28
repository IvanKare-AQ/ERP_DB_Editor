import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './FilterDialog.css'

function FilterDialog({ isOpen, onClose, onApply, allColumns = [] }) {
  const [filters, setFilters] = useState({})
  const [uniqueValues, setUniqueValues] = useState({})

  useEffect(() => {
    if (isOpen) {
      // Initialize filters for all columns
      const initialFilters = {}
      allColumns.forEach(col => {
        initialFilters[col] = {
          type: 'contains',
          value: ''
        }
      })
      setFilters(initialFilters)
      loadUniqueValues()
    }
  }, [isOpen, allColumns])

  const loadUniqueValues = async () => {
    try {
      const response = await axios.get('/api/database/load')
      if (response.data.success && response.data.data.items) {
        const values = {}
        allColumns.forEach(col => {
          const columnValues = new Set()
          response.data.data.items.forEach(item => {
            const val = item[col]
            if (val !== null && val !== undefined && val !== '') {
              columnValues.add(String(val))
            }
          })
          values[col] = Array.from(columnValues).sort()
        })
        setUniqueValues(values)
      }
    } catch (err) {
      console.error('Error loading unique values:', err)
    }
  }

  const handleFilterTypeChange = (column, type) => {
    setFilters(prev => ({
      ...prev,
      [column]: {
        ...prev[column],
        type
      }
    }))
  }

  const handleFilterValueChange = (column, value) => {
    setFilters(prev => ({
      ...prev,
      [column]: {
        ...prev[column],
        value
      }
    }))
  }

  const handleClearFilter = (column) => {
    setFilters(prev => ({
      ...prev,
      [column]: {
        type: 'contains',
        value: ''
      }
    }))
  }

  const handleClearAll = () => {
    const clearedFilters = {}
    allColumns.forEach(col => {
      clearedFilters[col] = {
        type: 'contains',
        value: ''
      }
    })
    setFilters(clearedFilters)
  }

  const handleApply = () => {
    // Filter out empty filters
    const activeFilters = {}
    Object.keys(filters).forEach(col => {
      if (filters[col].value && filters[col].value.trim() !== '') {
        activeFilters[col] = filters[col]
      }
    })
    onApply(activeFilters)
  }

  if (!isOpen) return null

  return (
    <div className="modal-overlay">
      <div className="modal-content filter-dialog">
        <h2>Filter Data</h2>
        <p>Set filters for columns to filter the tree view data:</p>
        
        <div className="filter-list">
          {allColumns.map(column => (
            <div key={column} className="filter-row">
              <label className="filter-column-label">{column}:</label>
              <select
                className="filter-type-select"
                value={filters[column]?.type || 'contains'}
                onChange={(e) => handleFilterTypeChange(column, e.target.value)}
              >
                <option value="contains">Contains</option>
                <option value="equals">Equals</option>
                <option value="starts_with">Starts With</option>
                <option value="ends_with">Ends With</option>
                <option value="not_contains">Not Contains</option>
              </select>
              <input
                type="text"
                className="filter-value-input"
                value={filters[column]?.value || ''}
                onChange={(e) => handleFilterValueChange(column, e.target.value)}
                placeholder="Enter filter value..."
                list={`datalist-${column}`}
              />
              <datalist id={`datalist-${column}`}>
                {uniqueValues[column]?.slice(0, 20).map(val => (
                  <option key={val} value={val} />
                ))}
              </datalist>
              <button
                className="btn-clear-filter"
                onClick={() => handleClearFilter(column)}
                title="Clear filter"
              >
                ✕
              </button>
            </div>
          ))}
        </div>

        <div className="modal-actions">
          <button className="btn-secondary" onClick={handleClearAll}>Clear All</button>
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleApply}>Apply Filters</button>
        </div>
      </div>
    </div>
  )
}

export default FilterDialog
