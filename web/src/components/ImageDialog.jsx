import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './ImageDialog.css'

function ImageDialog({ isOpen, onClose, onSelect, initialSearch = '' }) {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedImage, setSelectedImage] = useState(null)
  const [localFile, setLocalFile] = useState(null)

  // Update search query when dialog opens with new initialSearch
  useEffect(() => {
    if (isOpen && initialSearch) {
      setSearchQuery(initialSearch)
      setSearchResults([])
      setSelectedImage(null)
      setLocalFile(null)
    } else if (isOpen && !initialSearch) {
      setSearchQuery('')
      setSearchResults([])
      setSelectedImage(null)
      setLocalFile(null)
    }
  }, [isOpen, initialSearch])

  if (!isOpen) return null

  const handleWebSearch = async () => {
    if (!searchQuery.trim()) {
      alert('Please enter a search query')
      return
    }

    setLoading(true)
    setSearchResults([])
    setSelectedImage(null)
    
    try {
      const response = await axios.get('/api/images/search', {
        params: { query: searchQuery, max_results: 10 }
      })
      
      if (response.data.success && response.data.results && response.data.results.length > 0) {
        setSearchResults(response.data.results)
      } else {
        alert('No images found. Please try a different search term or use "Local File" option.')
        setSearchResults([])
      }
    } catch (err) {
      console.error('Error searching images:', err)
      const errorMsg = err.response?.data?.detail || err.message || 'Unknown error'
      alert(`Failed to search images: ${errorMsg}\n\nPlease try again or use "Local File" option.`)
      setSearchResults([])
    } finally {
      setLoading(false)
    }
  }

  const handleLocalFile = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.onchange = async (e) => {
      const file = e.target.files[0]
      if (file) {
        setLocalFile(file)
        setSelectedImage(URL.createObjectURL(file))
      }
    }
    input.click()
  }

  const handleSelectImage = async () => {
    if (selectedImage) {
      // If it's a local file, upload it first
      if (localFile) {
        const formData = new FormData()
        formData.append('file', localFile)
        
        try {
          const response = await axios.post('/api/images/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          
          if (response.data.success && response.data.file_path) {
            onSelect(response.data.file_path)
            onClose()
          } else {
            alert('Image upload not yet fully implemented. Using local path.')
            // For now, use a placeholder path
            onSelect(`Images/${localFile.name}`)
            onClose()
          }
        } catch (err) {
          console.error('Error uploading image:', err)
          alert('Failed to upload image. Using local path.')
          onSelect(`Images/${localFile.name}`)
          onClose()
        }
      } else if (selectedImage.startsWith('http')) {
        // Web image - download and save it
        try {
          // Download the image
          const downloadResponse = await axios.post('/api/images/download', {
            url: selectedImage,
            search_query: searchQuery
          }, {
            responseType: 'json'
          })
          
          if (downloadResponse.data.success && downloadResponse.data.file_path) {
            onSelect(downloadResponse.data.file_path)
            onClose()
          } else {
            alert('Failed to download and save image. Please try again or use "Local File" option.')
          }
        } catch (err) {
          console.error('Error downloading image:', err)
          alert('Failed to download image. Please try again or use "Local File" option.')
        }
      }
    }
  }

  const handleSelectWebImage = (imageUrl) => {
    setSelectedImage(imageUrl)
  }

  return (
    <div className="image-dialog-overlay" onClick={onClose}>
      <div className="image-dialog" onClick={(e) => e.stopPropagation()}>
        <h2>Add Image to Item</h2>
        
        <div className="image-dialog-search">
          <label>Search:</label>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Enter search phrase..."
            className="image-dialog-input"
          />
          <button onClick={handleWebSearch} disabled={loading} className="btn-search">
            {loading ? 'Searching...' : 'Search Web'}
          </button>
          <button onClick={handleLocalFile} className="btn-local">
            Local File
          </button>
        </div>

        {selectedImage && (
          <div className="image-dialog-preview">
            <h3>Selected Image:</h3>
            <img src={selectedImage} alt="Selected" className="preview-image" />
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="image-dialog-results">
            <h3>Search Results ({searchResults.length}):</h3>
            <div className="image-results-grid">
              {searchResults.map((result, index) => (
                <div
                  key={index}
                  className={`image-result-item ${selectedImage === result.url ? 'selected' : ''}`}
                  onClick={() => handleSelectWebImage(result.url)}
                >
                  <img 
                    src={result.thumbnail || result.url} 
                    alt={result.title || 'Result'}
                    onError={(e) => {
                      // Fallback if thumbnail fails
                      if (result.url && result.url !== result.thumbnail) {
                        e.target.src = result.url
                      }
                    }}
                  />
                  <p>{result.title || result.source || 'Image'}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {!loading && searchResults.length === 0 && searchQuery && (
          <div className="image-dialog-no-results">
            <p>No images found. Try a different search term.</p>
          </div>
        )}

        <div className="image-dialog-actions">
          <button onClick={onClose} className="btn-cancel">Cancel</button>
          <button 
            onClick={handleSelectImage} 
            className="btn-select"
            disabled={!selectedImage}
          >
            Select Image
          </button>
        </div>
      </div>
    </div>
  )
}

export default ImageDialog
