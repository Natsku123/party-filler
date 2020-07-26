import React, { useState, useEffect } from 'react'
import {
  TextField,
  Button,
} from '@material-ui/core'
import {
  DateTimePicker,
  MuiPickersUtilsProvider,
} from '@material-ui/pickers'
import MomentUtils from '@date-io/moment';

import SplitButton from '../SplitButton'

import partyService from '../../services/parties'
import channelService from '../../services/channels'

const initialChannels = [
  "none",
  "chess",
  "gw",
  "dotka",
]

const PartyForm = () => {
  const [ title, setTitle ] = useState('')
  const [ selectedChannel, setSelectedChannel ] = useState(0)
  const [ leaderId, setLeaderId ] = useState(1)
  const [ game, setGame ] = useState('Dota 2')
  const [ maxPlayers, setMaxPlayers ] = useState(5)
  const [ minPlayers, setMinPlayers ] = useState(5)
  const [ description, setDescription ] = useState('')
  const [ channelId, setChannelId ] = useState(5)
  const [ startTime, setStartTime ] = useState(new Date())
  const [ endTime, setEndTime ] = useState(new Date())

  const [ channels, setChannels ] = useState(null)

  useEffect(() => {
    setChannels(initialChannels)
    /*
     * Wait for backend to implement 'get all channels'
    channelService
      .getAll()
      .then(res => setChannels(res))
      */
  }, [])

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
    setStartTime(new Date())
    setEndTime(new Date())

    // setChannelId(5)
  }

  return (
    <form onSubmit={createParty}>
      <div>
        <TextField label="title" value={title} onChange={({target}) => setTitle(target.value)}/>
      </div>
      <div>
        { channels ?
            <div>
              channel:
              <SplitButton options={channels} selected={selectedChannel} setSelected={setSelectedChannel}/>
            </div> :
            <div>loading channels...</div>
        }
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
          <DateTimePicker label="End Time" value={endTime} onChange={setEndTime}/>
        </div>
      </MuiPickersUtilsProvider>

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
