import React from 'react'


const inputFields = ['email']


export default function CollaboratorForm({ formEmailData, handleSubmitCollaborator, handleEmailChange }) {

  return <div className="section">
    <div className="container">
      <form onSubmit={handleSubmitCollaborator}>
        
        {inputFields.map(field => {

          return <div key={field} className="field">
            <label className="label">
              {field[0].toUpperCase() + field.slice(1)}
            </label>
            <div className="control">
              <input
                className="input"
                type="text"
                value={formEmailData[field]}
                onChange={handleEmailChange}
                name={field}
              />
            </div>
          </div>
        })}
        <p>For adding collaborators into this folder, please insert email addresses above.</p>

        <button className="button mt-5">Add the collaborator</button>
      </form>
    </div>
  </div>
}