import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

import partyService from '../services/parties'

const Parties = () => {
  const [ parties, setParties ] = useState([])

  useEffect(() => {
    partyService
      .getAll()
      .then(data => {
        setParties(data)
      })
  }, [])


  const padding = {
    padding: 5
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Game</th>
          <th>Members</th>
          <th />
        </tr>
      </thead>
      <tbody>
        {parties.map((party, i) => 
          <tr key={i}>
            <td style={padding} >{party.title}</td>
            <td style={padding} >{party.game}</td>
            <td style={padding} >{`${party.members.length}`}</td>
            <td style={padding} >
              <Link to={`/parties/${party.id}`}>
                <button type='button'>show</button>
              </Link>
            </td>
          </tr>
        )}
      </tbody>
    </table>
  )
}

export default Parties
