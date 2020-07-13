import React, { useState } from 'react'

import partyService from '../../services/parties'

const PartyEdit = ({ party, setEdit, setParty }) => {
  const [ title, setTitle ] = useState(party.title)
  const [ leaderId, setLeaderId ] = useState(party.leaderId)
  const [ game, setGame ] = useState(party.game)
  const [ maxPlayers, setMaxPlayers ] = useState(party.maxPlayers)
  const [ minPlayers, setMinPlayers ] = useState(party.maxPlayers)
  const [ description, setDescription ] = useState(party.description)

  const editParty = (event) => {
    event.preventDefault()
    const newParty = {
      party: {
        title,
        leaderId,
        game,
        maxPlayers,
        minPlayers,
        description,
      }
    }

    partyService
      .update(party.id, newParty)
      .then(res => setParty(res))
    setEdit(false)
  }

  return (
    <form onSubmit={editParty}>
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
      {/*
      <div>
        Channel Id: <input type='number' value={channelId} onChange={({target}) => setChannelId(target.value)}/>
      </div>
      */}
      <button type='submit'>Create Party</button>
    </form>
  )
}

export default PartyEdit
