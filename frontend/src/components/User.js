import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'
import {
  Avatar,
} from '@material-ui/core'

import playerService from '../services/users'

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  small: {
    width: theme.spacing(3),
    height: theme.spacing(3),
  },
  large: {
    width: theme.spacing(7),
    height: theme.spacing(7),
  },
}))


const User = () => {
  const id = useParams().id
  const [ user, setUser ] = useState(null)
  const classes = useStyles()

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
      <Avatar alt={user.name} src={`https://cdn.discordapp.com/avatars/${user.discordId}/${user.icon}`} className={classes.large}/>
      <br />
      {user.name}
    </div>
  )
}

export default User
