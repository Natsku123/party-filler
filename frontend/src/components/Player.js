import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles'
import {
  Avatar,
} from '@material-ui/core'

import { playerService } from '../services/players'
import Glass from './Glass'

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


const Player = (props) => {
  const id = useParams().id
  const [ user, setUser ] = useState(null)
  const classes = useStyles()

  useEffect(() => {
    playerService
      .getOne(id)
      .then(res => setUser(res), error => props.onError(error.response.data.detail));
  }, [ props, id ])

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

export default Player
