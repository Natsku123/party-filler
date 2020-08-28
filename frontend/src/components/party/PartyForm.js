import React, { useState } from 'react'
import {
  TextField,
  Button,
} from '@material-ui/core'

import partyService from '../../services/parties'

const PartyForm = () => {
  // TODO: custom hook, fix time
  const [ title, setTitle ] = useState('')
  const [ leaderId, setLeaderId ] = useState(1)
  const [ game, setGame ] = useState('Dota 2')
  const [ maxPlayers, setMaxPlayers ] = useState(5)
  const [ minPlayers, setMinPlayers ] = useState(5)
  const [ description, setDescription ] = useState('')
  const [ channelId, setChannelId ] = useState(5)
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

    // setChannelId(5)
    // setStartTime('')
    // setEndTime('')
  }

  return (
    <form onSubmit={createParty}>
      <div>
        <TextField label="title" value={title} onChange={({target}) => setTitle(target.value)}/>
      </div>
      <div>
        <TextField label="Leader Id" type='number' value={leaderId} onChange={({target}) => setLeaderId(target.value)}/>
      </div>
      <div>
        <TextField label="Game" value={game} onChange={({target}) => setGame(target.value)}/>
      </div>
      <div>
        <TextField label="Max Players" type='number' min='1' value={maxPlayers} onChange={({target}) => setMaxPlayers(target.value)}/>
      </div>
      <div>
        <TextField label="Min Players" type='number' min='1' value={minPlayers} onChange={({target}) => setMinPlayers(target.value)}/>
      </div>
      <div>
        <TextField label="Description" value={description} onChange={({target}) => setDescription(target.value)}/>
      </div>
      {/*
      <div>
        <TextField label="Channel Id" type='number' value={channelId} onChange={({target}) => setChannelId(target.value)}/>
      </div>
      */}
      <Button variant='contained' color='primary' type='submit'>Create Party</Button>
    </form>
  )
}

export default PartyForm