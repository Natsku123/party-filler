import React, { useState, useEffect } from 'react'

import partyService from '../services/parties'

const initialParties = [
  {
    title: 'Battle Gauntlet Tier I',
    game: 'Dota 2',
    number: 5,
    players: 2
  },
  {
    title: 'Battle Gauntlet Tier II',
    game: 'Dota 2',
    number: 5,
    players: 3
  }, 
  {
    title: 'Chess Tournament',
    game: 'Chess',
    number: 4,
    players: 1
  }
]

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

  console.log(parties)

  return (
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Game</th>
          <th>Players</th>
        </tr>
      </thead>
      <tbody>
        {parties.map((party, i) => 
          <tr key={i}>
            <td style={padding} >{party.title}</td>
            <td style={padding} >{party.game}</td>
            <td style={padding} >{`${party.players} / ${party.number}`}</td>
          </tr>
        )}
      </tbody>
    </table>
  )
}

export default Parties
