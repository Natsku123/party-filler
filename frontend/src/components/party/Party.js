import React, { useState, useEffect } from 'react';
import { useParams, useHistory, Link } from 'react-router-dom';
import {
  Button,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Grid,
} from '@material-ui/core';

import PartyEdit from './PartyEdit';
import DiscordAvatar from '../DiscordAvatar';


import { partyService } from '../../services/parties';
import { joinParty, leaveParty } from '../../services/utils';
import { playerService } from '../../services/players';

const Party = (props) => {
  const id = useParams().id;
  const history = useHistory();
  const [ party, setParty ] = useState(null);
  const [ members, setMembers ] = useState([]);
  const [ user, setUser ] = useState(null);
  const [ edit, setEdit ] = useState(false);
  const [ member, setMember ] = useState();

  useEffect(() => {
    partyService
      .getOne(id)
      .then(res => setParty(res))
      .catch(error => props.onError(error.response.data.detail));
  }, [props, id ]);

  useEffect(() => {
    partyService
      .getMembers(id)
      .then(res => setMembers(res))
      .catch(error => props.onError(error.response.data.detail));
  }, [props, id ]);

  useEffect(() => {
    playerService
      .getCurrent()
      .then(res => setUser(res))
      .catch(error => props.onError(error.response.data.detail));
  }, [props]);

  if (!party) {
    return <div>loading...</div>;
  }

  const isMember = user && members
    .find((member) => member.player.id === user.id);

  const isLeader = user && user.id === party.leaderId;

  const join = (roleId) => {
    const notify = window.confirm('Do you want discord notifications?');

    joinParty(party.id, user.id, roleId, party.min_players, notify)
      .then(member => {
        setMembers(members.concat(member));
        setMember(member);
        props.onSuccess('Successfully joined ' + party.title + '!');
      }).catch(error => props.onError(error.response.data.detail));
  };

  const leave = () => {
    leaveParty(member.id)
      .then(removedMember => {
        setMembers(members.filter(member => member.id !== removedMember.id));
        props.onSuccess('Successfully left ' + party.title + '!');
      }).catch(error => props.onError(error.response.data.detail));
  };

  const remove = () => {
    partyService
      .remove(id)
      .then(removedParty => {
        history.push('/parties');
        props.onSuccess('Successfully deleted ' + party.title + '!');
      }).catch(error => props.onError(error.response.data.detail));
  };

  if (isLeader && edit) {
    return <PartyEdit
      party={party}
      setEdit={setEdit}
      setParty={setParty}
      onError={props.onError}
      onSuccess={props.onSuccess}
    />;
  }

  return (
    <div>
      <h1>
        {party.title}
        { isLeader &&
          <> - You are the leader
            <Button variant='contained' color='secondary' onClick={ remove }>Delete</Button>
          </>
        }
      </h1>
      <div>
        { isLeader &&
        <Button variant='contained' color='primary' onClick={ () => setEdit(true) }>Edit</Button>
        }
        { !isLeader &&
          <>
            { isMember ?
              <Button variant='contained' color='secondary' onClick={leave}>Leave</Button> :
              <Button variant='contained' color='primary' onClick={join}>Join</Button>
            }
          </>
        }
      </div>
      <h2>Information</h2>
      <Grid container direction='column' spacing={4}>
        <Grid item container spacing={2}>
          <Grid item>Game: {party.game.name}</Grid>
          <Grid item>Max Players: {party.maxPlayers}</Grid>
          <Grid item>Min Players: {party.minPlayers}</Grid>
        </Grid>
        <Grid item>Description: {party.description}</Grid>
        <Grid item>Start Time: {party.startTime}</Grid>
        <Grid item>End Time: {party.endTime}</Grid>
        <Grid item>Channel: {party.channel.name} @ {party.channel.server.name}</Grid>
      </Grid>
      <h2>Members</h2>
      <List>
        <ListItem key={0}>
          <ListItemAvatar>
            <DiscordAvatar user={party.leader} size='small' />
          </ListItemAvatar>
          <ListItemText primary={party.leader.name} secondary="Leader" />
        </ListItem>
        {members.map(member => {
          return (
            <ListItem key={member.id}>
              <ListItemAvatar>
                <DiscordAvatar user={party.leader} size='small' />
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
