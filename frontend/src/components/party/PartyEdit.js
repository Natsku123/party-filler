import React, { useState } from 'react'
import {
  TextField,
  Button,
} from '@material-ui/core'

import partyService from '../../services/parties'

const PartyEdit = ({ party, setEdit, setParty }) => {
  const [ title, setTitle ] = useState(party.title)
  const [ leaderId, setLeaderId ] = useState(party.leaderId)
  const [ game, setGame ] = useState(party.game)
  const [ maxPlayers, setMaxPlayers ] = useState(party.maxPlayers)
  const [ minPlayers, setMinPlayers ] = useState(party.maxPlayers)
  const [ description, setDescription ] = useState(party.description)
  const [ startTime, setStartTime ] = useState(new Date())
  const [ endTime, setEndTime ] = useState(new Date())

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
        startTime,
        endTime,
      }
    }

    partyService
      .update(party.id, newParty)
      .then(res => setParty(res))
    setEdit(false)
  }

  const cancel = (event) => {
    setEdit(false)
  }

  return (
    <div>
      <div>
        <TextField label="Title" value={title} onChange={({target}) => setTitle(target.value)}/>
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
        <TextField label="Description" value={description} onChange={({target}) => setDescription(target.value)} multiline/>
      </div>
      <MuiPickersUtilsProvider utils={MomentUtils}>
        <div>
          <DateTimePicker label="Start Time" value={startTime} onChange={setStartTime}/>
        </div>
        <div>
          <TextField label="End Time" value={endTime} onChange={setEndTime}/>
        </div>
      </MuiPickersUtilsProvider>

      {/*
      <div>
        <TextField label="Channel Id" type='number' value={channelId} onChange={({target}) => setChannelId(target.value)}/>
      </div>
      */}
      <Button variant='contained' color='primary' onClick={editParty}>Save</Button>
      <Button variant='contained' color='secondary' onClick={cancel}>Cancel</Button>
    </div>
  )
}

export default PartyEdit
