import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import partyService from '../services/parties'
import userService from '../services/users'

const Party = () => {
  const id = useParams().id
  const [ party, setParty ] = useState(null)
  const [ user, setUser ] = useState(null)

  useEffect(() => {
    partyService
      .getOne(id)
      .then(res => setParty(res))
  }, [ id ])

  useEffect(() => {
    userService
      .getUser()
      .then(res => setUser(res))
  }, [])

  if (!party) {
    return <div>loading...</div>
  }

  const isMember = user && party.members
    .map((member) => member.id)
    .includes(user.id)

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
      .then(member => setParty({
        ...party,
        members: party.members.concat(member),
      }))
  }

  const leave = () => {
    partyService
      .join(party.id, user.id)
      .then(res => {
        if (res.status === "success") {
          setParty({
            ...party,
            members: party.members.filter(member => member.id !== user.id),
          })
        }
      })
  }

  return (
    <div>
      <h1>Party</h1>
      { !user ?
          <p>Et ole kirjautunut</p> :
          <div>
            { user.id === party.leaderId ?
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
      <ol>
        {party.members.map(member => <li key={member}>{member.name}</li>)}
      </ol>
    </div>
  )
}

export default Party
