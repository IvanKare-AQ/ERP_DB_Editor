import React, { useState, useEffect } from 'react'
import axios from 'axios'
import ImageDialog from './ImageDialog'
import './ManualEditor.css'

function ManualEditor({ selectedItem, onItemUpdate, onClearSelection }) {
  // ERP Name fields
  const [userErpName, setUserErpName] = useState('')
  const [type, setType] = useState('')
  const [pn, setPn] = useState('')
  const [details, setDetails] = useState('')
  
  // Other fields
  const [manufacturer, setManufacturer] = useState('')
  const [remark, setRemark] = useState('')
  const [serialized, setSerialized] = useState(false)
  const [buy, setBuy] = useState(false)
  
  // Category fields
  const [category, setCategory] = useState('')
  const [subcategory, setSubcategory] = useState('')
  const [subSubcategory, setSubSubcategory] = useState('')
  
  // Original values for reset
  const [originalErpName, setOriginalErpName] = useState('')
  const [originalManufacturer, setOriginalManufacturer] = useState('')
  const [originalRemark, setOriginalRemark] = useState('')
  const [originalCategory, setOriginalCategory] = useState('')
  const [originalSubcategory, setOriginalSubcategory] = useState('')
  const [originalSubSubcategory, setOriginalSubSubcategory] = useState('')
  
  // Categories data
  const [categories, setCategories] = useState({ categories: [], subcategories: {}, subSubcategories: {} })
  const [availableSubcategories, setAvailableSubcategories] = useState([])
  const [availableSubSubcategories, setAvailableSubSubcategories] = useState([])
  
  // Image state
  const [imageUrl, setImageUrl] = useState(null)
  const [imageError, setImageError] = useState(false)
  const [imagePath, setImagePath] = useState('')
  const [showImageDialog, setShowImageDialog] = useState(false)
  const [imageSearchTerm, setImageSearchTerm] = useState('')
  
  // New item mode
  const [isNewItemMode, setIsNewItemMode] = useState(false)
  const [pnEditable, setPnEditable] = useState(false)
  const [airQPn, setAirQPn] = useState(null) // AirQ_PN database ID for new items
  const [airQPnValid, setAirQPnValid] = useState(true) // Validation state for AirQ PN
  const [airQPnChecking, setAirQPnChecking] = useState(false) // Loading state for validation

  useEffect(() => {
    loadCategories()
  }, [])

  useEffect(() => {
    // Initialize editor with next available AirQ PN when no item is selected and not in new item mode
    if (!selectedItem && !isNewItemMode && airQPn === null) {
      initializeEditor()
    }
  }, [selectedItem, isNewItemMode])

  const initializeEditor = async () => {
    try {
      // Get next available AirQ_PN (database ID)
      const response = await axios.get('/api/items/next-pn')
      const nextAirQPn = response.data.pn || 1
      setAirQPn(nextAirQPn)
      setAirQPnValid(true)
      setAirQPnChecking(false)
      
      // Clear all fields
      setUserErpName('')
      setType('')
      setPn('') // Clear Mfr. PN
      setDetails('')
      setManufacturer('')
      setRemark('')
      setSerialized(false)
      setBuy(true)
      setCategory('')
      setSubcategory('')
      setSubSubcategory('')
      setImagePath('')
      setImageUrl(null)
      setImageError(false)
      setAvailableSubcategories([])
      setAvailableSubSubcategories([])
      
      // Clear original values
      setOriginalErpName('')
      setOriginalManufacturer('')
      setOriginalRemark('')
      setOriginalCategory('')
      setOriginalSubcategory('')
      setOriginalSubSubcategory('')
    } catch (err) {
      console.error('Error initializing editor:', err)
      setAirQPn(null)
      setAirQPnValid(true)
      setAirQPnChecking(false)
    }
  }

  useEffect(() => {
    // Don't populate fields if in new item mode - let handleNew control the fields
    if (isNewItemMode && !selectedItem) {
      return // Keep fields as set by handleNew
    }
    
    if (selectedItem) {
      try {
        // Exit new item mode when an item is selected
        if (isNewItemMode) {
          setIsNewItemMode(false)
          setPnEditable(false)
          setAirQPn(null) // Clear AirQ_PN state
        }
        
        // Parse ERP Name object
        const erpNameObj = selectedItem['ERP Name'] || {}
        const fullName = typeof erpNameObj === 'string' ? erpNameObj : (erpNameObj?.full_name || '')
        const typeValue = typeof erpNameObj === 'object' ? (erpNameObj?.type || '') : ''
        const pnValue = typeof erpNameObj === 'object' ? (erpNameObj?.part_number || '') : ''
        const detailsValue = typeof erpNameObj === 'object' ? (erpNameObj?.additional_parameters || '') : ''
        
        setUserErpName(fullName)
        setType(typeValue)
        setPn(pnValue)
        setDetails(detailsValue)
        setOriginalErpName(fullName)
        
        setManufacturer(selectedItem.Manufacturer || '')
        setOriginalManufacturer(selectedItem.Manufacturer || '')
        
        setRemark(selectedItem.Remark || '')
        setOriginalRemark(selectedItem.Remark || '')
        
        setSerialized(selectedItem.Serialized === 'Yes')
        setBuy(selectedItem.Buy === 'Yes')
        
        const cat = selectedItem.Category || ''
        const subcat = selectedItem.Subcategory || ''
        const subsubcat = selectedItem['Sub-subcategory'] || ''
        
        setCategory(cat)
        setSubcategory(subcat)
        setSubSubcategory(subsubcat)
        setOriginalCategory(cat)
        setOriginalSubcategory(subcat)
        setOriginalSubSubcategory(subsubcat)
        
        // Load subcategories for this category
        if (cat && categories.subcategories[cat]) {
          setAvailableSubcategories(categories.subcategories[cat])
          if (subcat && categories.subSubcategories[`${cat}::${subcat}`]) {
            setAvailableSubSubcategories(categories.subSubcategories[`${cat}::${subcat}`])
          }
        }
        
        // Load image
        const imgPath = selectedItem.Image || ''
        setImagePath(imgPath)
        if (imgPath) {
          // Encode the image path for URL
          const encodedPath = encodeURIComponent(imgPath)
          setImageUrl(`/api/images/${encodedPath}`)
          setImageError(false)
        } else {
          setImageUrl(null)
          setImageError(false)
        }
      } catch (err) {
        console.error('Error setting selected item:', err)
      }
    } else if (!isNewItemMode) {
      // Clear all fields only if not in new item mode
      setUserErpName('')
      setType('')
      setPn('')
      setDetails('')
      setManufacturer('')
      setRemark('')
      setSerialized(false)
      setBuy(false)
      setCategory('')
      setSubcategory('')
      setSubSubcategory('')
      setAvailableSubcategories([])
      setAvailableSubSubcategories([])
      setImageUrl(null)
      setImageError(false)
      setImagePath('')
    }
  }, [selectedItem, categories])

  const handleNew = async () => {
    try {
      // Set new item mode FIRST to prevent useEffect from overwriting
      setIsNewItemMode(true)
      setPnEditable(true)
      
      // Get next available AirQ_PN (database ID)
      const response = await axios.get('/api/items/next-pn')
      const nextAirQPn = response.data.pn || 1
      setAirQPn(nextAirQPn)
      setAirQPnValid(true) // Reset validation state
      setAirQPnChecking(false)
      
      // Clear all fields AFTER setting new item mode
      // Mfr. PN (pn) should be blank, not set to AirQ_PN
      setUserErpName('')
      setType('')
      setPn('') // Clear Mfr. PN - this is separate from AirQ_PN
      setDetails('')
      setManufacturer('')
      setRemark('')
      setSerialized(false)
      setBuy(true)
      setCategory('')
      setSubcategory('')
      setSubSubcategory('')
      setImagePath('')
      setImageUrl(null)
      setImageError(false)
      setAvailableSubcategories([])
      setAvailableSubSubcategories([])
      
      // Clear original values
      setOriginalErpName('')
      setOriginalManufacturer('')
      setOriginalRemark('')
      setOriginalCategory('')
      setOriginalSubcategory('')
      setOriginalSubSubcategory('')
    } catch (err) {
      console.error('Error getting next PN:', err)
      // Set mode first even on error
      setIsNewItemMode(true)
      setPnEditable(true)
      alert('Failed to get next AirQ PN. Please enter a value manually.')
      setAirQPn(null) // Let user enter manually
      setAirQPnValid(true) // Reset validation
      setAirQPnChecking(false)
      setPn('') // Clear Mfr. PN
    }
  }

  const handleAddItem = async () => {
    if (!userErpName.trim()) {
      alert('ERP Name is required.')
      return
    }

    if (!category || !subcategory || !subSubcategory || 
        category === 'Select Category...' || 
        subcategory === 'Select Subcategory...' || 
        subSubcategory === 'Select Sub-subcategory...') {
      alert('Please choose Category, Subcategory, and Sub-subcategory.')
      return
    }
    
    // Validate PN uniqueness if in new item mode
    if (isNewItemMode && pn) {
      try {
        const pnValue = parseInt(pn)
        if (isNaN(pnValue)) {
          alert('PN must be a valid number.')
          return
        }
        
        const checkResponse = await axios.get(`/api/items/check-pn/${pnValue}`)
        if (!checkResponse.data.available) {
          alert(`PN ${String(pnValue).padStart(7, '0')} already exists. Please use a different PN.`)
          return
        }
      } catch (err) {
        console.error('Error checking PN:', err)
        // Continue anyway if check fails
      }
    }

    try {
      const erpNameObj = {
        full_name: userErpName,
        type: type,
        part_number: pn,
        additional_parameters: details
      }

      // Determine Buy value - if manufacturer contains "AirQ", set to "No"
      let buyValue = buy
      if (manufacturer.includes('AirQ')) {
        buyValue = false
      }

      // Get AirQ_PN value - use airQPn state if in new item mode or no item selected, otherwise get next available
      let pnValue = null
      if (isNewItemMode || !selectedItem) {
        // Validate AirQ PN before proceeding
        if (!airQPnValid) {
          alert('AirQ PN already exists. Please enter a unique value.')
          return
        }
        // Use the AirQ_PN that was set when "New" button was clicked, initialized, or entered by user
        pnValue = airQPn
        if (!pnValue) {
          // If user cleared it, get next available
          try {
            const response = await axios.get('/api/items/next-pn')
            pnValue = response.data.pn || 1
          } catch (err) {
            console.error('Error getting next PN:', err)
            alert('Failed to get next AirQ PN.')
            return
          }
        }
      }

      const newItem = {
        erp_name: erpNameObj,
        manufacturer,
        remark,
        category,
        subcategory,
        sub_subcategory: subSubcategory,
        serialized: serialized ? 'Yes' : 'No',
        buy: buyValue ? 'Yes' : 'No',
        image: imagePath,
        pn: pnValue
      }

      const response = await axios.post('/api/items/', newItem)
      
      if (response.data.success) {
        const pnFormatted = String(response.data.data.pn).padStart(7, '0')
        alert(`Draft item PN ${pnFormatted} saved to the add queue.`)
        
        // Reset form
        setUserErpName('')
        setType('')
        setPn('')
        setDetails('')
        setManufacturer('')
        setRemark('')
        setSerialized(false)
        setBuy(true)
        setCategory('')
        setSubcategory('')
        setSubSubcategory('')
        setImagePath('')
        setImageUrl(null)
        setAvailableSubcategories([])
        setAvailableSubSubcategories([])
        setIsNewItemMode(false)
        setPnEditable(false)
        setAirQPn(null) // Clear AirQ_PN state
        setAirQPnValid(true) // Reset validation
        setAirQPnChecking(false)
        
        if (onItemUpdate) {
          onItemUpdate()
        }
      }
    } catch (err) {
      console.error('Error adding item:', err)
      alert('Failed to add item')
    }
  }

  const handleImport = () => {
    alert('Import functionality coming soon')
  }

  const handleAddImage = () => {
    // Use PN as search term, or Details if PN is "NO-PN"
    let searchTerm = ''
    if (pn && pn.trim().toUpperCase() !== 'NO-PN') {
      searchTerm = pn.trim()
    } else if (details && details.trim()) {
      searchTerm = details.trim()
    } else {
      searchTerm = userErpName || ''
    }
    setShowImageDialog(true)
    // Store search term to pass to dialog
    setImageSearchTerm(searchTerm)
  }

  const handleImageSelected = (path) => {
    setImagePath(path)
    const encodedPath = encodeURIComponent(path)
    setImageUrl(`/api/images/${encodedPath}`)
    setImageError(false)
    
    // If item is selected, update it
    if (selectedItem) {
      // Update will be saved when user clicks "Update All Fields"
    }
  }

  const loadCategories = async () => {
    try {
      const response = await axios.get('/api/categories/unique')
      if (response.data.success) {
        setCategories({
          categories: response.data.categories || [],
          subcategories: response.data.subcategories || {},
          subSubcategories: response.data.sub_subcategories || {}
        })
      }
    } catch (err) {
      console.error('Error loading categories:', err)
    }
  }

  // Parse User ERP Name into Type, PN, Details
  const parseUserErpName = (erpName) => {
    if (!erpName) {
      setType('')
      setPn('')
      setDetails('')
      return
    }
    
    const parts = erpName.split('_', 3)
    setType(parts[0] || '')
    setPn(parts[1] || '')
    setDetails(parts[2] || '')
  }

  // Reconstruct User ERP Name from Type, PN, Details
  const reconstructErpName = () => {
    const parts = []
    if (type) parts.push(type)
    if (pn) parts.push(pn)
    if (details) parts.push(details)
    return parts.join('_')
  }

  const handleUserErpNameChange = (value) => {
    setUserErpName(value)
    parseUserErpName(value)
  }

  const handleTypeChange = (value) => {
    setType(value)
    setUserErpName(reconstructErpName())
  }

  const handlePnChange = (value) => {
    // Only allow numeric input for PN
    if (value === '' || /^\d+$/.test(value)) {
      setPn(value)
      // Only update ERP Name if not in new item mode (to preserve user input)
      if (!isNewItemMode) {
        setUserErpName(reconstructErpName())
      }
    }
  }

  const handleAirQPnChange = async (value) => {
    // Only allow numeric input for AirQ PN
    if (value === '' || /^\d+$/.test(value)) {
      const numValue = value === '' ? null : parseInt(value)
      setAirQPn(numValue)
      
      // Validate if value is provided
      if (value && value.trim() !== '') {
        setAirQPnChecking(true)
        try {
          const checkResponse = await axios.get(`/api/items/check-pn/${value}`)
          setAirQPnValid(checkResponse.data.available)
        } catch (err) {
          console.error('Error checking AirQ PN:', err)
          setAirQPnValid(true) // Assume valid on error to not block user
        } finally {
          setAirQPnChecking(false)
        }
      } else {
        setAirQPnValid(true) // Empty is valid (will use next available)
      }
    }
  }

  const handleDetailsChange = (value) => {
    setDetails(value)
    setUserErpName(reconstructErpName())
  }

  const handleCategoryChange = (value) => {
    setCategory(value)
    setSubcategory('')
    setSubSubcategory('')
    if (value && categories.subcategories[value]) {
      setAvailableSubcategories(categories.subcategories[value])
    } else {
      setAvailableSubcategories([])
    }
    setAvailableSubSubcategories([])
  }

  const handleSubcategoryChange = (value) => {
    setSubcategory(value)
    setSubSubcategory('')
    if (value && category && categories.subSubcategories[`${category}::${value}`]) {
      setAvailableSubSubcategories(categories.subSubcategories[`${category}::${value}`])
    } else {
      setAvailableSubSubcategories([])
    }
  }

  const convertUnderscoresToHyphens = (field, setter) => {
    const value = field.replace(/_/g, '-')
    setter(value)
    if (setter === setType) handleTypeChange(value)
    else if (setter === setPn) handlePnChange(value)
    else if (setter === setDetails) handleDetailsChange(value)
  }

  const insertNoPn = () => {
    setPn('NO-PN')
    handlePnChange('NO-PN')
  }

  const resetErpName = () => {
    setUserErpName(originalErpName)
    parseUserErpName(originalErpName)
  }

  const resetManufacturer = () => {
    setManufacturer(originalManufacturer)
  }

  const resetRemark = () => {
    setRemark(originalRemark)
  }

  const resetCategoryDropdowns = () => {
    setCategory(originalCategory)
    setSubcategory(originalSubcategory)
    setSubSubcategory(originalSubSubcategory)
    if (originalCategory && categories.subcategories[originalCategory]) {
      setAvailableSubcategories(categories.subcategories[originalCategory])
      if (originalSubcategory && categories.subSubcategories[`${originalCategory}::${originalSubcategory}`]) {
        setAvailableSubSubcategories(categories.subSubcategories[`${originalCategory}::${originalSubcategory}`])
      }
    }
  }

  const handleUpdate = async () => {
    if (!selectedItem && !isNewItemMode) return

    try {
      const erpNameObj = {
        full_name: userErpName,
        type: type,
        part_number: pn,
        additional_parameters: details
      }

      const updateData = {
        row_id: selectedItem._id,
        erp_name: erpNameObj,
        manufacturer,
        remark,
        category,
        subcategory,
        sub_subcategory: subSubcategory,
        serialized: serialized ? 'Yes' : 'No',
        buy: buy ? 'Yes' : 'No',
        image: imagePath
      }

      await axios.put(`/api/items/${selectedItem._id}`, updateData)
      if (onItemUpdate) {
        onItemUpdate()
      }
    } catch (err) {
      console.error('Error updating item:', err)
      alert('Failed to update item')
    }
  }

  const handleReassign = async () => {
    if ((!selectedItem && !isNewItemMode) || !category || !subcategory || !subSubcategory) return

    try {
      await axios.post('/api/items/reassign', {
        row_id: selectedItem._id,
        category,
        subcategory,
        sub_subcategory: subSubcategory
      })
      
      setOriginalCategory(category)
      setOriginalSubcategory(subcategory)
      setOriginalSubSubcategory(subSubcategory)
      
      if (onItemUpdate) {
        onItemUpdate()
      }
    } catch (err) {
      console.error('Error reassigning item:', err)
      alert('Failed to reassign item')
    }
  }

  const handleDelete = async () => {
    if (!selectedItem || isNewItemMode) return
    
    if (!confirm(`Are you sure you want to delete this item?\n\nERP Name: ${userErpName}\nThis action cannot be undone.`)) {
      return
    }

    try {
      await axios.delete(`/api/items/${selectedItem._id}`)
      if (onItemUpdate) {
        onItemUpdate()
      }
    } catch (err) {
      console.error('Error deleting item:', err)
      alert('Failed to delete item')
    }
  }

  const handleSuggest = async () => {
    if (!type && !pn && !details) {
      alert('Please provide at least Type, Part Number, or Details for category suggestion.')
      return
    }

    try {
      const response = await axios.post('/api/categories/suggest', {
        current_category: category || null,
        type_value: type,
        part_number: pn,
        details: details,
        model_name: 'llama3.2',
        use_ai: true
      })

      if (response.data.success && response.data.suggestion) {
        const suggestion = response.data.suggestion
        
        if (suggestion.valid) {
          // Apply suggestion directly
          setCategory(suggestion.category)
          setSubcategory(suggestion.subcategory)
          setSubSubcategory(suggestion.sub_subcategory)
          
          // Update available dropdowns
          if (categories.subcategories[suggestion.category]) {
            setAvailableSubcategories(categories.subcategories[suggestion.category])
            if (categories.subSubcategories[`${suggestion.category}::${suggestion.subcategory}`]) {
              setAvailableSubSubcategories(categories.subSubcategories[`${suggestion.category}::${suggestion.subcategory}`])
            }
          }
        } else {
          // Ask user if they want to use the suggestion anyway
          const useAnyway = confirm(
            `The suggested category path may not exist:\n\n` +
            `Category: ${suggestion.category}\n` +
            `Subcategory: ${suggestion.subcategory}\n` +
            `Sub-subcategory: ${suggestion.sub_subcategory}\n\n` +
            `Would you like to apply it anyway?`
          )
          
          if (useAnyway) {
            setCategory(suggestion.category)
            setSubcategory(suggestion.subcategory)
            setSubSubcategory(suggestion.sub_subcategory)
          }
        }
      } else {
        alert('Could not generate category suggestion. Please try again or select manually.')
      }
    } catch (err) {
      console.error('Error getting category suggestion:', err)
      alert('Category suggestion feature is not yet fully implemented')
    }
  }

  const canReassign = category && subcategory && subSubcategory && 
    (category !== originalCategory || subcategory !== originalSubcategory || subSubcategory !== originalSubSubcategory)

  // Calculate AirQ PN display - use airQPn if in new item mode or if no item selected, otherwise use selected item's AirQ_PN
  const currentPn = isNewItemMode ? (airQPn || 0) : (selectedItem ? selectedItem.AirQ_PN : (airQPn || 0))
  const pnDisplay = String(currentPn || 0).padStart(7, '0')

  return (
    <div className="manual-editor">
      {/* Image Preview with Action Buttons */}
      <div className="image-preview-section">
        <div className="image-preview-container">
          {imageUrl && !imageError ? (
            <img 
              src={imageUrl} 
              alt="Item preview"
              className="image-preview-img"
              onError={() => {
                setImageError(true)
                setImageUrl(null)
              }}
            />
          ) : (
            <div className="image-preview">
              {imageError ? 'Image\nNot Found' : 'No Image'}
            </div>
          )}
        </div>
        <div className="image-action-buttons-vertical">
          <button className="btn-action" onClick={handleImport}>Import</button>
          <button className="btn-action" onClick={handleAddImage}>Add Image</button>
        </div>
      </div>
      
      {/* PN Label and Main Action Buttons */}
      <div className="image-action-row">
        <div className="pn-label-container">
          <label className="pn-label">AirQ PN:</label>
          {isNewItemMode || !selectedItem ? (
            <input
              type="text"
              value={airQPn || ''}
              onChange={(e) => handleAirQPnChange(e.target.value)}
              className={`editor-input airq-pn-input ${!airQPnValid ? 'invalid' : ''}`}
              placeholder="Enter AirQ PN..."
              disabled={airQPnChecking}
            />
          ) : (
            <span className="pn-value">{pnDisplay}</span>
          )}
        </div>
        <div className="image-action-buttons">
          <button className="btn-action" onClick={handleNew}>New</button>
          <button className="btn-action" onClick={handleAddItem}>← Add Item</button>
        </div>
      </div>

      {/* ERP Name Section */}
      <div className="editor-section">
        <div className="editor-field">
          <label>ERP Name:</label>
          <div className="field-with-button">
            <input
              type="text"
              value={userErpName}
              onChange={(e) => handleUserErpNameChange(e.target.value)}
              className="editor-input"
              placeholder="Enter ERP Name..."
            />
            <button 
              className="btn-reset"
              onClick={resetErpName}
              disabled={userErpName === originalErpName}
            >
              Reset
            </button>
          </div>
        </div>

        <div className="editor-field">
          <label>Type:</label>
          <div className="field-with-button">
            <input
              type="text"
              value={type}
              onChange={(e) => handleTypeChange(e.target.value)}
              className="editor-input"
              placeholder="Enter Type..."
            />
            <button 
              className="btn-convert"
              onClick={() => convertUnderscoresToHyphens(type, setType)}
            >
              _ → -
            </button>
          </div>
        </div>

        <div className="editor-field">
          <label>Mfr. PN:</label>
          <div className="field-with-buttons">
            <input
              type="text"
              value={pn}
              onChange={(e) => handlePnChange(e.target.value)}
              className="editor-input"
              placeholder="Enter Mfr. PN..."
              disabled={!pnEditable}
              readOnly={!pnEditable}
            />
            <button 
              className="btn-convert"
              onClick={() => convertUnderscoresToHyphens(pn, setPn)}
            >
              _ → -
            </button>
            <button 
              className="btn-no-pn"
              onClick={insertNoPn}
            >
              NO-PN
            </button>
          </div>
        </div>

        <div className="editor-field">
          <label>Details:</label>
          <div className="field-with-buttons">
            <input
              type="text"
              value={details}
              onChange={(e) => handleDetailsChange(e.target.value)}
              className="editor-input"
              placeholder="Enter Details..."
            />
            <button 
              className="btn-convert"
              onClick={() => convertUnderscoresToHyphens(details, setDetails)}
            >
              _ → -
            </button>
            <button 
              className="btn-convert-update"
              onClick={() => {
                convertUnderscoresToHyphens(details, setDetails)
                handleUpdate()
              }}
            >
              _ → - + Update
            </button>
          </div>
        </div>
      </div>

      <div className="editor-separator"></div>

      {/* Manufacturer and Remark */}
      <div className="editor-section">
        <div className="editor-field">
          <label>Manufacturer:</label>
          <div className="field-with-button">
            <input
              type="text"
              value={manufacturer}
              onChange={(e) => setManufacturer(e.target.value)}
              className="editor-input"
              placeholder="Enter Manufacturer..."
            />
            <button 
              className="btn-reset"
              onClick={resetManufacturer}
              disabled={manufacturer === originalManufacturer}
            >
              Reset
            </button>
          </div>
        </div>

        <div className="editor-field">
          <label>Remark:</label>
          <div className="field-with-button">
            <input
              type="text"
              value={remark}
              onChange={(e) => setRemark(e.target.value)}
              className="editor-input"
              placeholder="Enter Remark..."
            />
            <button 
              className="btn-reset"
              onClick={resetRemark}
              disabled={remark === originalRemark}
            >
              Reset
            </button>
          </div>
        </div>
      </div>

      <div className="editor-separator"></div>

      {/* Update and Delete Buttons with Serialized and Buy */}
      <div className="editor-actions">
        {isNewItemMode ? (
          <button onClick={handleAddItem} className="btn-update">
            Add Item
          </button>
        ) : (
          <>
            <button onClick={handleUpdate} className="btn-update">
              Update All Fields
            </button>
            <button onClick={handleDelete} className="btn-delete">
              Delete Selected Item
            </button>
          </>
        )}
        <div className="checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={serialized}
              onChange={(e) => setSerialized(e.target.checked)}
            />
            Serialized
          </label>
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={buy}
              onChange={(e) => setBuy(e.target.checked)}
            />
            Buy
          </label>
        </div>
      </div>

      <div className="editor-separator"></div>

      {/* Reassignment Section */}
      <div className="reassignment-section">
        <div className="reassignment-columns">
          <div className="reassignment-left">
            <div className="editor-field">
              <label>Category:</label>
              <select
                value={category}
                onChange={(e) => handleCategoryChange(e.target.value)}
                className="editor-select"
              >
                <option value="">Select Category...</option>
                {categories.categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="editor-field">
              <label>Subcategory:</label>
              <select
                value={subcategory}
                onChange={(e) => handleSubcategoryChange(e.target.value)}
                className="editor-select"
                disabled={!category}
              >
                <option value="">Select Subcategory...</option>
                {availableSubcategories.map(sub => (
                  <option key={sub} value={sub}>{sub}</option>
                ))}
              </select>
            </div>

            <div className="editor-field">
              <label>Sub-subcategory:</label>
              <select
                value={subSubcategory}
                onChange={(e) => setSubSubcategory(e.target.value)}
                className="editor-select"
                disabled={!subcategory}
              >
                <option value="">Select Sub-subcategory...</option>
                {availableSubSubcategories.map(subsub => (
                  <option key={subsub} value={subsub}>{subsub}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="reassignment-right">
            <button 
              onClick={handleSuggest} 
              className="btn-suggest"
            >
              Suggest
            </button>
            <button 
              onClick={handleReassign} 
              className="btn-reassign"
              disabled={!canReassign}
            >
              Reassign
            </button>
            <button 
              onClick={resetCategoryDropdowns} 
              className="btn-reset-category"
              disabled={!canReassign}
            >
              Reset
            </button>
          </div>
        </div>
      </div>

      {/* Image Dialog */}
      <ImageDialog
        isOpen={showImageDialog}
        onClose={() => {
          setShowImageDialog(false)
          setImageSearchTerm('')
        }}
        onSelect={handleImageSelected}
        initialSearch={imageSearchTerm}
      />
    </div>
  )
}

export default ManualEditor
