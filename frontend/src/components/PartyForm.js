import React, { useState } from 'react'

const PartyForm = () => {
  const [ title, setTitle ] = useState('')
  const [ game, setGame ] = useState('')
  const [ number, setNumber ] = useState(5)

  const createParty = (event) => {
    event.preventDefault()
    const gameObject = { 
      title: title,
      game: game,
      number: number,
      players: 0
    }

    console.log('New Game:', JSON.stringify(gameObject))
    setTitle('')
    setGame('')
    setNumber(5)
  }

  return (
    <form onSubmit={createParty}>
      <div>
        Title: <input value={title} onChange={({target}) => setTitle(target.value)}/>
      </div>
      <div>
        Game: <input value={game} onChange={({target}) => setGame(target.value)}/>
      </div>
      <div>
        Players: <input type='number' min='1' value={number} onChange={({target}) => setNumber(target.value)}/>
      </div>
      <button type='submit'>Create Party</button>
    </form>
  )
}

export default PartyForm
