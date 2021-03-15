import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'
export default function Workspace() {
  const [folders, updateFolders] = useState([])



  useEffect(() => {
    async function getFolderData() {
      try {
        const { data } = await axios.get('/api/folders')
        updateFolders(data)
      } catch (err) {
        console.log(err)
      }
    }
    getFolderData()
  }, [])

  return <div>

    <div className="container">
      <div className="columns is-multiline is-mobile">
        {folders.map((folder, index) => {
          return <div key={index} className="column is-one-third-desktop is-half-tablet is-half-mobile">
            <Link to={`/folders/${folder.id}`}>
              <div className="card">
                <div className="card-content">
                  <div className="media">
                    <div className="media-content">
                      <p className="title is-4">{folder.name}</p>
                    </div>
                  </div>
                </div>
              </div>
            </Link>
          </div>
        })}
      </div>
    </div>
  </div>

}