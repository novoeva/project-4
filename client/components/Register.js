import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function Register({ history }) {

  const [formData, updateFormData] = useState({
    username: '',
    email: '',
    password: ''
    // passwordConfirmation: ''
  })

  const [errors, updateErrors] = useState({
    username: '',
    email: '',
    password: ''
    // passwordConfirmation: ''
  })

  function handleChange(event) {
    const { name, value } = event.target
    updateFormData({ ...formData, [name]: value })
    updateErrors({ ...errors, [name]: '' })
  }
  // useEffect(() => {
  //   axios.get('/api/test')
  //     .then(resp => {
  //       console.log(resp.data)
  //     })
        
  // }, [])



  async function handleSubmit(event) {
    event.preventDefault()
    try {
      const { data } = await axios.post('/api/signup', formData)
      // console.log(data)

      history.push('/login')
    } catch (err) {
      updateErrors(err.response.data.errors)
      // console.log(errors)
    }
  }
  // console.log(formData)

  return <div className="section">
    <div className="container" id="container-form">
      <form onSubmit={handleSubmit} id='registration-form'>
        <div className="field">
          <label className="label">Username</label>
          <div className="control">
            <input
              className="input"
              type="text"
              value={formData.username}
              onChange={handleChange}
              name={'username'}
            />

            {errors.username && <small className="has-text-danger">
              {errors.username}
            </small>}
          </div>
        </div>
        <div className="field">
          <label className="label">Email</label>
          <div className="control">
            <input
              className="input"
              type="text"
              value={formData.email}
              onChange={handleChange}
              name={'email'}
            />

            {errors.email && <small className="has-text-danger">
              {errors.email}
            </small>}
          </div>
        </div>
        <div className="field">
          <label className="label">Password</label>
          <div className="control">
            <input
              className="input"
              type="password"
              value={formData.password}
              onChange={handleChange}
              name={'password'}
            />

            {errors.password && <small className="has-text-danger">
              {errors.password}
            </small>}
          </div>
        </div>
        {/* <div className="field">
          <label className="label">Confirm password</label>
          <div className="control">
            <input
              className="input"
              type="password"
              value={formData.passwordConfirmation}
              onChange={handleChange}
              name={'passwordConfirmation'}
            />
            
            {errors.passwordConfirmation && <small className="has-text-danger">
              {errors.passwordConfirmation}
            </small>}
          </div> */}
        {/* </div> */}
        <button className="button">Submit</button>
      </form>
    </div>
  </div>
}