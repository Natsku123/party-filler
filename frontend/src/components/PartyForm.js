import React, { useState } from 'react'

import partyService from '../services/parties'

const PartyForm = () => {
  // TODO: custom hook, fix time
  const [ title, setTitle ] = useState('')
  const [ leaderId, setLeaderId ] = useState(1)
  const [ game, setGame ] = useState('Dota 2')
  const [ maxPlayers, setMaxPlayers ] = useState(5)
  const [ minPlayers, setMinPlayers ] = useState(5)
  const [ description, setDescription ] = useState('')
  const [ channelId, setChannelId ] = useState('')
  const [ startTime, setStartTime ] = useState('1996-10-15T00:05:32.000Z')
  const [ endTime, setEndTime ] = useState('1996-10-15T00:05:32.000Z')

  const createParty = (event) => {
    event.preventDefault()
    const partyObject = {
      "party": {
        title,
        leaderId,
        game,
        maxPlayers,
        minPlayers,
        description,
        channelId,
        startTime,
        endTime,
      }
    }

    partyService.create(partyObject)

    setTitle('')
    setLeaderId(2)
    setGame('Dota 2')
    setMaxPlayers(5)
    setMinPlayers(5)
    setDescription('')
    setChannelId(5)

    // setStartTime('')
    // setEndTime('')
  }

  return (
    <form onSubmit={createParty}>
      <div>
        Title: <input value={title} onChange={({target}) => setTitle(target.value)}/>
      </div>
      <div>
        Leader Id: <input type='number' value={leaderId} onChange={({target}) => setLeaderId(target.value)}/>
      </div>
      <div>
        Game: <input value={game} onChange={({target}) => setGame(target.value)}/>
      </div>
      <div>
        Max Players: <input type='number' min='1' value={maxPlayers} onChange={({target}) => setMaxPlayers(target.value)}/>
      </div>
      <div>
        Min Players: <input type='number' min='1' value={minPlayers} onChange={({target}) => setMinPlayers(target.value)}/>
      </div>
      <div>
        Description: <input value={description} onChange={({target}) => setDescription(target.value)}/>
      </div>
      <div>
        Channel Id: <input value={channelId} onChange={({target}) => setChannelId(target.value)}/>
      </div>
      <button type='submit'>Create Party</button>
    </form>
  )
}

export default PartyForm
