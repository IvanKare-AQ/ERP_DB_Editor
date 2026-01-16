import React, { useState, useEffect, useMemo } from 'react'
import axios from 'axios'
import './TreeView.css'

function TreeView({ onItemSelect, selectedItemId }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expandedNodes, setExpandedNodes] = useState(new Set())
  const [visibleColumns, setVisibleColumns] = useState([])

  useEffect(() => {
    loadDatabase()
  }, [])

  const loadDatabase = async () => {
    try {
      setLoading(true)
      const response = await axios.get('/api/database/load')
      if (response.data.success) {
        setData(response.data.data.items)
        setVisibleColumns(response.data.data.columns || [])
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
                        let pn = '0000000'
                        let erpName = 'No Name'
                        
                        try {
                          pn = String(item.AirQ_PN || '').padStart(7, '0')
                          const erpNameObj = item['ERP Name']
                          if (typeof erpNameObj === 'string') {
                            erpName = erpNameObj
                          } else if (erpNameObj && typeof erpNameObj === 'object') {
                            erpName = erpNameObj.full_name || erpNameObj.type || 'No Name'
                          }
                        } catch (err) {
                          console.error('Error processing item:', err, item)
                        }
                        
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
                            <span className="tree-item-pn">{pn}</span>
                            <span className="tree-item-name">{erpName}</span>
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

  return (
    <div className="tree-view">
      {renderTree()}
    </div>
  )
}

export default TreeView
