import React, { useState, useEffect } from 'react';
import Moment from 'react-moment';
import 'moment-timezone';
import moment from 'moment/moment';
import { useParams, useHistory, Link } from 'react-router-dom';
import {
  Button,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Grid, withStyles, Typography, Box,
} from '@material-ui/core';

import PartyEdit from './PartyEdit';
import DiscordAvatar from '../DiscordAvatar';

import { partyService } from '../../services/parties';
import { joinParty, leaveParty } from '../../services/utils';
import { playerService } from '../../services/players';
import { Skeleton } from '@material-ui/lab';
import { makeStyles } from '@material-ui/core/styles';
import { toDate } from '../DatetimeTools';


const PartyTitle = withStyles({
  root: {
    fontFamily: 'Montserrat',
    fontSize: '37px',
    fontStyle: 'normal',
    fontWeight: 700,
    lineHeight: '45px',
    letterSpacing: '0em',
    textAlign: 'center'
  }
})(Typography);

const ParticipationText = withStyles({
  root: {
    fontFamily: 'Montserrat',
    fontSize: '28px',
    fontStyle: 'normal',
    fontWeight: 400,
    lineHeight: '34px',
    letterSpacing: '0em',
    textAlign: 'center'
  }
})(Typography);

const TimeText = withStyles({
  root: {
    fontFamily: 'Montserrat',
    fontSize: '20px',
    fontStyle: 'normal',
    fontWeight: 400,
    lineHeight: '24px',
    letterSpacing: '0em',
    textAlign: 'center'
  }
})(Typography);

const MemberName = withStyles({
  root: {
    fontFamily: 'Montserrat',
    fontSize: '24px',
    fontStyle: 'normal',
    fontWeight: 500,
    lineHeight: '40px',
    letterSpacing: '0em',
    textAlign: 'left'
  }
})(Typography);

const MemberRole = withStyles({
  root: {
    fontFamily: 'Montserrat',
    fontSize: '18px',
    fontStyle: 'normal',
    fontWeight: 400,
    lineHeight: '29px',
    letterSpacing: '0em',
    textAlign: 'left',
    color: '#4F4F4F'
  }
})(Typography);

const InfoTitle = withStyles({
  root: {
    fontFamily: 'Montserrat',
    fontSize: '34px',
    fontStyle: 'normal',
    fontWeight: 700,
    lineHeight: '41px',
    letterSpacing: '0em',
    textAlign: 'left',
  }
})(Typography);

const useStyles = makeStyles(() => ({
  bodyText: {
    fontFamily: 'Montserrat',
    fontSize: '23px',
    fontStyle: 'normal',
    fontWeight: 400,
    lineHeight: '28px',
    letterSpacing: '0em',
    textAlign: 'left'
  }
}));

const Party = (props) => {
  const id = useParams().id;
  const history = useHistory();
  const classes = useStyles();
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
    return (
      <div>
        <PartyTitle variant={'h1'}><Skeleton /></PartyTitle>
        <ParticipationText variant={'h2'}><Skeleton /></ParticipationText>
      </div>
    );
  }

  const isMember = user && members
    .find((member) => member.player.id === user.id);

  const isLeader = user && user.id === party.leaderId;

  const join = () => {
    const notify = window.confirm('Do you want discord notifications?');

    // Todo role selection by popup if any roles configured?
    const roleId = null;

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
        props.onSuccess('Successfully deleted ' + removedParty.title + '!');
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
      <PartyTitle variant={'h1'}>{party.title}</PartyTitle>
      { isLeader
        ? <ParticipationText variant={'h2'}>You are the leader</ParticipationText>
        : <ParticipationText variant={'h2'}>You are a member</ParticipationText>
      }
      <TimeText variant={'h3'}>{toDate(party.endTime) >= new Date() ? 'Ending' : 'Ended'} <Moment fromNow>{toDate(party.endTime)}</Moment></TimeText>
      <Grid container spacing={2} justify={'center'} style={{ marginTop: '5px' }}>
        { isLeader &&
          <>
            <Grid item><Button variant='contained' color='primary' onClick={ () => setEdit(true) }>Edit</Button></Grid>
            <Grid item><Button variant='contained' color='secondary' onClick={ remove }>Delete</Button></Grid>
          </>
        }
        { !isLeader &&
          <>
            { isMember ?
              <Grid item><Button variant='contained' color='secondary' onClick={leave}>Leave</Button></Grid> :
              <Grid item><Button variant='contained' color='primary' onClick={join}>Join</Button></Grid>
            }
          </>
        }
      </Grid>
      <Box py={2}/>
      <Grid container>
        <Grid item md={8} xs={12}>
          <InfoTitle variant={'h4'}>Information</InfoTitle>
          <Grid container direction='column' spacing={4} justify={'center'}>
            <Grid item container spacing={2}>
              <Grid item className={classes.bodyText}>Game: {party.game.name}</Grid>
            </Grid>
            <Grid item container spacing={2}>
              <Grid item className={classes.bodyText}>Max Players: {party.maxPlayers}</Grid>
              <Grid item className={classes.bodyText}>Min Players: {party.minPlayers}</Grid>
            </Grid>
            <Grid item container spacing={2}>
              <Grid item className={classes.bodyText}>Description: {party.description}</Grid>
            </Grid>
            <Grid item container spacing={2}>
              <Grid item className={classes.bodyText}>Start Time: <Moment local calendar>{toDate(party.startTime)}</Moment></Grid>
              <Grid item className={classes.bodyText}>End Time: <Moment local calendar>{toDate(party.endTime)}</Moment></Grid>
            </Grid>
            <Grid item container spacing={2}>
              <Grid item className={classes.bodyText}>Channel: {party.channel.name} @ {party.channel.server.name}</Grid>
            </Grid>
          </Grid>
        </Grid>
        <Grid item md={4} xs={12}>
          <InfoTitle variant={'h3'}>Members</InfoTitle>
          <Box py={2}>
            <Grid container direction={'column'} spacing={4}>
              {members.map(member => {
                return (
                  <Grid item xs container direction={'row'} key={member.id} spacing={2} alignItems={'center'}>
                    <Grid item>
                      <DiscordAvatar user={member.player} size='xxl' />
                    </Grid>
                    <Grid item xs container direction={'column'}>
                      <Grid item>
                        <MemberName>{member.player.name}</MemberName>
                      </Grid>
                      <Grid item>
                        <MemberRole>{
                          member.roleId ? member.player.id === party.leader.id ? 'Leader - ' + member.role.name : 'Member - ' + member.role.name : member.player.id === party.leader.id ? 'Leader' : 'Member'
                        }</MemberRole>
                      </Grid>
                    </Grid>
                  </Grid>
                );
              })}
            </Grid>
          </Box>
        </Grid>
      </Grid>
    </div>
  );
};

export default Party;
