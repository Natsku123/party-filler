import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Button,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar
} from '@material-ui/core';

import PartyEdit from './PartyEdit';
import Glass from '../Glass';


import { partyService } from '../../services/parties';
import { joinParty, leaveParty } from '../../services/utils';
import { playerService } from '../../services/players';

const Party = (props) => {
  const id = useParams().id;
  const [ party, setParty ] = useState(null);
  const [ members, setMembers ] = useState([]);
  const [ user, setUser ] = useState(null);
  const [ edit, setEdit ] = useState(false);
  const [ member, setMember ] = useState();

  useEffect(() => {
    partyService
      .getOne(id)
      .then(res => setParty(res), error => props.onError(error.response.data.detail));
  }, [props, id ]);

  useEffect(() => {
    partyService
      .getMembers(id)
      .then(res => setMembers(res), error => props.onError(error.response.data.detail));
  }, [props, id ]);

  useEffect(() => {
    playerService
      .getCurrent()
      .then(res => setUser(res), error => props.onError(error.response.data.detail));
  }, [props]);

  if (!party) {
    return <div>loading...</div>;
  }

  const isMember = user && members
    .map((member) => member.player.id)
    .includes(user.id);

  const isLeader = user && user.id === party.leaderId;

  const join = (roleId) => {
    const notify = window.confirm('Do you want discord notifications?');

    joinParty(party.id, user.id, roleId, party.min_players, notify)
      .then(member => {
        setMembers(members.concat(member));
        setMember(member);
        props.onSuccess('Successfully joined ' + party.title + '!');
      }, error => props.onError(error.response.data.detail));
  };

  const leave = () => {

    leaveParty(member.id)
      .then(removedMember => {
        setMembers(members.filter(member => member.id !== removedMember.id));
        props.onSuccess('Successfully left ' + party.title + '!');
      }, error => props.onError(error.response.data.detail));
  };

  if (isLeader && edit) {
    return <PartyEdit
      party={party}
      setEdit={setEdit}
      setParty={setParty}
    />;
  }

  return (
    <div>
      <h1>{party.title}</h1>
      { !user ?
        <p>Et ole kirjautunut</p> :
        <div>
          { isLeader ?
            <div>
              <p>Olet johtaja</p>
              <Button variant='contained' color='primary' onClick={ () => setEdit(true) }>Edit</Button>
            </div> :
            <div>
              { isMember ?
                <Button variant='contained' color='secondary' onClick={leave}>Leave</Button> :
                <Button variant='contained' color='primary' onClick={join}>Join</Button>
              }
            </div>
          }

        </div>
      }
      <h2>Information</h2>
      <p>Game: {party.game.name}</p>
      <p>Max Players: {party.maxPlayers}</p>
      <p>Min Players: {party.minPlayers}</p>
      <p>Description: {party.description}</p>
      <p>Start Time: {party.startTime}</p>
      <p>End Time: {party.endTime}</p>
      <p>Channel: {party.channel.name} @ {party.channel.server.name}</p>
      <h2>Members</h2>
      <List>
        <ListItem key={0}>
          <ListItemAvatar>
            <Avatar alt={party.leader.name} src={`https://cdn.discordapp.com/avatars/${party.leader.discordId}/${party.leader.icon}`} />
          </ListItemAvatar>
          <ListItemText primary={party.leader.name} secondary="Leader" />
        </ListItem>
        {members.map(member => {
          return (
            <ListItem key={member.id}>
              <ListItemAvatar>
                <Avatar alt={member.player.name} src={`https://cdn.discordapp.com/avatars/${member.player.discordId}/${member.player.icon}`} />
              </ListItemAvatar>
              <ListItemText primary={member.player.name} secondary="Member" />
            </ListItem>
          );
        })}
      </List>
    </div>
  );
};

export default Party;
