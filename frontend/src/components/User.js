import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import playerService from '../services/players'

const User = () => {
  const id = useParams().id
  const [ user, setUser ] = useState(null)

  useEffect(() => {
    playerService
      .getUserById(id)
      .then(res => setUser(res))
  }, [ id ])

  if (!user) {
    return <div>loading...</div>
  }

  return (
    <div>
      <img src={`https://cdn.discordapp.com/avatars/${user.discord_id}/${user.icon}`} alt="user icon"/>
      <br />
      {user.name}
    </div>
  )
}

export default User
