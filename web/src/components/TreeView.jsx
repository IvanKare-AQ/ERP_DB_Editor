import React, { useState, useEffect, useMemo } from 'react'
import axios from 'axios'
import './TreeView.css'

function TreeView({ onItemSelect, selectedItemId, visibleColumns = [], currentView = 'primary' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expandedNodes, setExpandedNodes] = useState(new Set())
  const [allColumns, setAllColumns] = useState([])

  useEffect(() => {
    loadDatabase()
  }, [currentView])

  useEffect(() => {
    // Reload when visibleColumns change
    if (data && visibleColumns.length > 0) {
      // Force re-render with new column visibility
    }
  }, [visibleColumns, data])

  const loadDatabase = async () => {
    try {
      setLoading(true)
      let response
      if (currentView === 'added') {
        response = await axios.get('/api/database/load-added')
      } else {
        response = await axios.get('/api/database/load')
      }
      
      if (response.data.success) {
        setData(response.data.data.items)
        setAllColumns(response.data.data.columns || [])
        setError(null)
      } else {
        setError('Failed to load database')
      }
    } catch (err) {
      setError(`Error loading database: ${err.message}`)
      console.error('Database load error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getColumnValue = (item, columnName) => {
    try {
      if (columnName === 'ERP Name') {
        const erpNameObj = item['ERP Name']
        if (typeof erpNameObj === 'string') {
          return erpNameObj
        } else if (erpNameObj && typeof erpNameObj === 'object') {
          return erpNameObj.full_name || erpNameObj.type || ''
        }
        return ''
      } else if (columnName === 'AirQ_PN') {
        const pn = item.AirQ_PN || ''
        return String(pn).padStart(7, '0')
      } else {
        return item[columnName] || ''
      }
    } catch (err) {
      console.error(`Error getting column value for ${columnName}:`, err)
      return ''
    }
  }

  const getDisplayColumns = () => {
    // If visibleColumns is provided and not empty, use it
    // Otherwise, use all columns
    if (visibleColumns && visibleColumns.length > 0) {
      return visibleColumns
    }
    return allColumns
  }

  // Build hierarchical structure
  const treeData = useMemo(() => {
    if (!data || data.length === 0) return []

    const tree = {}
    
    data.forEach((item, index) => {
      const category = item.Category || 'Uncategorized'
      const subcategory = item.Subcategory || 'Uncategorized'
      const subSubcategory = item['Sub-subcategory'] || 'Uncategorized'
      
      if (!tree[category]) {
        tree[category] = {}
      }
      if (!tree[category][subcategory]) {
        tree[category][subcategory] = {}
      }
      if (!tree[category][subcategory][subSubcategory]) {
        tree[category][subcategory][subSubcategory] = []
      }
      
      tree[category][subcategory][subSubcategory].push({
        ...item,
        _index: index,
        _id: `item-${index}`
      })
    })
    
    return tree
  }, [data])

  const toggleNode = (path) => {
    const newExpanded = new Set(expandedNodes)
    if (newExpanded.has(path)) {
      newExpanded.delete(path)
    } else {
      newExpanded.add(path)
    }
    setExpandedNodes(newExpanded)
  }

  const renderTree = () => {
    if (loading) {
      return <div className="tree-loading">Loading database...</div>
    }
    
    if (error) {
      return <div className="tree-error">Error: {error}</div>
    }
    
    if (!treeData || Object.keys(treeData).length === 0) {
      return <div className="tree-empty">No data available</div>
    }

    const nodes = []
    
    Object.keys(treeData).sort().forEach(category => {
      const categoryPath = `cat-${category}`
      const isCategoryExpanded = expandedNodes.has(categoryPath)
      
      nodes.push(
        <div key={categoryPath} className="tree-node">
          <div 
            className="tree-node-header"
            onClick={() => toggleNode(categoryPath)}
          >
            <span className="tree-toggle">{isCategoryExpanded ? '▼' : '▶'}</span>
            <span className="tree-label">{category}</span>
          </div>
          
          {isCategoryExpanded && Object.keys(treeData[category]).sort().map(subcategory => {
            const subcategoryPath = `${categoryPath}-sub-${subcategory}`
            const isSubcategoryExpanded = expandedNodes.has(subcategoryPath)
            
            return (
              <div key={subcategoryPath} className="tree-node tree-node-child">
                <div 
                  className="tree-node-header"
                  onClick={() => toggleNode(subcategoryPath)}
                >
                  <span className="tree-toggle">{isSubcategoryExpanded ? '▼' : '▶'}</span>
                  <span className="tree-label">{subcategory}</span>
                </div>
                
                {isSubcategoryExpanded && Object.keys(treeData[category][subcategory]).sort().map(subSubcategory => {
                  const subSubcategoryPath = `${subcategoryPath}-subsub-${subSubcategory}`
                  const isSubSubcategoryExpanded = expandedNodes.has(subSubcategoryPath)
                  
                  return (
                    <div key={subSubcategoryPath} className="tree-node tree-node-child">
                      <div 
                        className="tree-node-header"
                        onClick={() => toggleNode(subSubcategoryPath)}
                      >
                        <span className="tree-toggle">{isSubSubcategoryExpanded ? '▼' : '▶'}</span>
                        <span className="tree-label">{subSubcategory}</span>
                      </div>
                      
                      {isSubSubcategoryExpanded && treeData[category][subcategory][subSubcategory].map(item => {
                        const itemId = item._id
                        const isSelected = selectedItemId === itemId
                        const displayColumns = getDisplayColumns()
                        
                        return (
                          <div
                            key={itemId}
                            className={`tree-item ${isSelected ? 'tree-item-selected' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation()
                              if (onItemSelect) {
                                try {
                                  onItemSelect(item, itemId)
                                } catch (err) {
                                  console.error('Error selecting item:', err)
                                }
                              }
                            }}
                          >
                            {displayColumns.length > 0 ? (
                              displayColumns.map((col, idx) => (
                                <span 
                                  key={col} 
                                  className={`tree-item-cell tree-item-${col.toLowerCase().replace(/\s+/g, '-')}`}
                                  style={{ minWidth: idx === 0 ? '80px' : '120px' }}
                                >
                                  {getColumnValue(item, col)}
                                </span>
                              ))
                            ) : (
                              <>
                                <span className="tree-item-pn">{getColumnValue(item, 'AirQ_PN')}</span>
                                <span className="tree-item-name">{getColumnValue(item, 'ERP Name')}</span>
                              </>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  )
                })}
              </div>
            )
          })}
        </div>
      )
    })
    
    return nodes
  }

  const displayColumns = getDisplayColumns()

  return (
    <div className="tree-view">
      {displayColumns.length > 0 && (
        <div className="tree-header">
          {displayColumns.map(col => (
            <span 
              key={col} 
              className={`tree-header-cell tree-header-${col.toLowerCase().replace(/\s+/g, '-')}`}
            >
              {col}
            </span>
          ))}
        </div>
      )}
      {renderTree()}
    </div>
  )
}

export default TreeView
