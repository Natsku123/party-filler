import React, { useState } from 'react'

import channelService from '../services/channels'

// nimi, discordId, serverId

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
        Name: <input value={name} onChange={({target}) => setName(target.value)}/>
      </div>
      <div>
        Discord Id: <input value={discordId} onChange={({target}) => setDiscordId(target.value)}/>
      </div>
      <div>
        Server Id: <input type='number' value={serverId} onChange={({target}) => setServerId(target.value)}/>
      </div>
      <button type='submit'>Create Channel</button>
    </form>
  )
}

export default ChannelForm
