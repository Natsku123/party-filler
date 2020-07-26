import React, { useState } from 'react'
import {
  TextField,
  Button,
} from '@material-ui/core'

import channelService from '../services/channels'

const ChannelForm = () => {
  const [ discordId, setDiscordId ] = useState('')

  const createChannel = (event) => {
    event.preventDefault()
    const channelObj = {
      channel: {
        discordId,
      }
    }

    channelService.create(channelObj)
    setDiscordId('')
  }

  return (
    <form onSubmit={createChannel}>
      <div>
        <TextField label="Discord Id" value={discordId} onChange={({target}) => setDiscordId(target.value)}/>
      </div>
      <Button variant='contained' color='primary' type='submit'>Create Channel</Button>
    </form>
  )
}

export default ChannelForm
