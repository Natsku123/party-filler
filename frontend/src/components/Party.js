import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import partyService from '../services/parties'

const Party = () => {
  const id = useParams().id
  const [ party, setParty ] = useState(null)

  useEffect(() => {
    partyService
      .getOne(id)
      .then(res => setParty(res))
  }, [])

  console.log(party)

  if (!party) {
    return <div>loading...</div>
  }

  return (
    <div>
      <h1>Party</h1>
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
        {party.members.map(member => <li>member.name)</li>)}
      </ol>
    </div>
  )
}

export default Party
