import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import partyService from '../services/parties'
import userService from '../services/users'

const Party = () => {
  const id = useParams().id
  const [ party, setParty ] = useState(null)
  const [ members, setMembers ] = useState([])
  const [ user, setUser ] = useState(null)
  const [ edit, setEdit ] = useState(false)

  useEffect(() => {
    partyService
      .getOne(id)
      .then(res => setParty(res))
  }, [ id ])

  useEffect(() => {
    partyService
      .getPlayers(id)
      .then(res => setMembers(res))
  }, [ id ])

  useEffect(() => {
    userService
      .getUser()
      .then(res => setUser(res))
  }, [])

  if (!party) {
    return <div>loading...</div>
  }

  const isMember = user && members
    .map((member) => member.player.id)
    .includes(user.id)

  const isLeader = user && user.id === party.leaderId

  const join = () => {
    const memberObj = {
      "member" : {
        partyReq: party.min_players,
        partyId: party.id,
        playerId: user.id,
      }
    }

    partyService
      .join(party.id, memberObj)
      .then(member => setMembers(members.concat(member)) )
  }

  const leave = () => {
    partyService
      .leave(party.id, user.id)
      .then(res => {
        if (res.status === "success") {
          setMembers(members.filter(member => member.id !== user.id))
        }
      })
  }

  if (isLeader && edit) {
  }

  return (
    <div>
      <h1>Party</h1>
      { !user ?
          <p>Et ole kirjautunut</p> :
          <div>
            { isLeader ?
                <p>Olet johtaja</p> :
                <p>Et ole johtaja</p>
            }
            { isMember ?
                <button onClick={leave}>Leave</button> :
                <button onClick={join}>Join</button>
            }
          </div>
      }
      <h2>Information</h2>
      <p>Party Id: {party.id}</p>
      <p>Title: {party.title}</p>
      <p>Game: {party.game}</p>
      <p>Max Players: {party.maxPlayers}</p>
      <p>Min Players: {party.minPlayers}</p>
      <p>Description: {party.description}</p>
      <p>Channel Id: {party.channelId}</p>
      <p>Start Time: {party.startTime}</p>
      <p>End Time: {party.endTime}</p>
      {/*
      <p>Channel: {party.channel.name}</p>
      <p>Leader: {party.leader.name}</p>
      */}
      <h2>Members</h2>
      <ul>
        {members.map(member => <li key={member}>{member.player.name}</li>)}
      </ul>
    </div>
  )
}

export default Party
