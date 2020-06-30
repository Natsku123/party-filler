import React from 'react'

const Party = (party) => {
  return (
    <div>
      <h1>Party</h1>
      <h2>Information</h2>
      <p>Party Id: {party.id}</p>
      <p>Title: {party.title}</p>
      <p>Game: {party.title}</p>
      <p>Max Players: {party.maxPlayers}</p>
      <p>Min Players: {party.minPlayers}</p>
      <p>Description: {party.description}</p>
      <p>Channel Id: {party.channelId}</p>
      <p>Start Time: {party.startTime}</p>
      <p>End Time: {party.endTime}</p>
      <p>Channel: {party.channel.name}</p>
      <p>Leader: {party.leader.name}</p>
      <h2>Players</h2>
      <ol>
        {party.players.map(player => <li>player.name)</li>)}
      </ol>
    </div>
  )
}

export default Party
