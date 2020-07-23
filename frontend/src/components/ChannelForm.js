import React, { useState } from 'react'
import {
  TextField,
  Button,
} from '@material-ui/core'

import channelService from '../services/channels'

const ChannelForm = () => {
  const [ name, setName ] = useState('')
  const [ discordId, setDiscordId ] = useState('')
  const [ serverId, setServerId ] = useState(0)


  const createChannel = (event) => {
    event.preventDefault()
    const channelObj = {
      channel: {
        name,
        discordId,
        serverId,
      }
    }

    channelService.create(channelObj)

    setName('')
    setDiscordId('')
    setServerId(0)
  }

  return (
    <form onSubmit={createChannel}>
      <div>
        <TextField label="Name" value={name} onChange={({target}) => setName(target.value)}/>
      </div>
      <div>
        <TextField label="Discord Id" value={discordId} onChange={({target}) => setDiscordId(target.value)}/>
      </div>
      <div>
        <TextField label="Server Id" type='number' value={serverId} onChange={({target}) => setServerId(target.value)}/>
      </div>
      <Button variant='contained' color='primary' type='submit'>Create Channel</Button>
    </form>
  )
}

export default ChannelForm
