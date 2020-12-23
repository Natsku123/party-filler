import React, { useState, useEffect } from 'react'
import {
  TextField,
  Button,
} from '@material-ui/core'
import {
  DateTimePicker,
  MuiPickersUtilsProvider,
} from '@material-ui/pickers'
import MomentUtils from '@date-io/moment';

import SplitButton from '../SplitButton'

import { partyService } from '../../services/parties'
import {playerService} from "../../services/players";
import {serverService} from "../../services/servers";

const PartyForm = (props) => {
  const [ title, setTitle ] = useState('')
  const [ selectedChannel, setSelectedChannel ] = useState(0)
  const [ leaderId, setLeaderId ] = useState(1)
  const [ game, setGame ] = useState('Dota 2')
  const [ maxPlayers, setMaxPlayers ] = useState(5)
  const [ minPlayers, setMinPlayers ] = useState(5)
  const [ description, setDescription ] = useState('')
  const [ channelId, setChannelId ] = useState(5)
  const [ startTime, setStartTime ] = useState(new Date())
  const [ endTime, setEndTime ] = useState(new Date())

  const [ channels, setChannels ] = useState(null)
  const [ chNames, setChNames ] = useState(["No channel"]);
  const [ currentUser, setCurrentUser ] = useState(null);

  useEffect(() => {
      let foundChannels = [];
      let channelNames = ["No channel"]
      playerService.getCurrent().then(r => {
          r.servers.forEach(server => {
              serverService.getChannels(server.id).then(res => {
                  res.forEach(c => {
                      foundChannels.push(c);
                      console.log(c);
                      channelNames.push(server.name + " - " + c.name);
                  });
              });
          });
          setChannels(foundChannels);
          setChNames(channelNames);
          setCurrentUser(r);

      }, e => {
          props.onError(e.response.detail);
      });
  }, [props])

  const createParty = (event) => {
    event.preventDefault()
    console.log(selectedChannel);
    let channelDetails;
    if (selectedChannel > 0) {
        channelDetails = channels[selectedChannel-1];
    } else {
        channelDetails = null;
    }

    let partyObject;
    if (channelDetails !== null) {
        setChannelId(channelDetails.id);

        partyObject = {
            title,
            leaderId,
            game,
            channelId,
            maxPlayers,
            minPlayers,
            description,
            startTime,
            endTime,
        }
    } else {
        partyObject = {
            title,
            leaderId,
            game,
            maxPlayers,
            minPlayers,
            description,
            startTime,
            endTime,
        }
    }

    partyService.create(partyObject).then(r => {
        props.onSuccess("Party " + r.title + " created.");
    }, e => {
        props.onError(e.response.detail);
    });

    setTitle('')
    setLeaderId(2)
    setGame('Dota 2')
    setMaxPlayers(5)
    setMinPlayers(5)
    setDescription('')
    setStartTime(new Date())
    setEndTime(new Date())

    // setChannelId(5)
  }

  return (
    <form onSubmit={createParty}>
      <div>
        <TextField label="title" value={title} onChange={({target}) => setTitle(target.value)}/>
      </div>
      <div>
        { channels ?
            <div>
              channel:
              <SplitButton options={chNames} selected={selectedChannel} setSelected={setSelectedChannel}/>
            </div> :
            <div>loading channels...</div>
        }
      </div>
      <div>
        <TextField label="Leader Id" type='number' value={leaderId} onChange={({target}) => setLeaderId(target.value)}/>
      </div>
      <div>
        <TextField label="Game" value={game} onChange={({target}) => setGame(target.value)}/>
      </div>
      <div>
        <TextField label="Max Players" type='number' min='1' value={maxPlayers} onChange={({target}) => setMaxPlayers(target.value)}/>
      </div>
      <div>
        <TextField label="Min Players" type='number' min='1' value={minPlayers} onChange={({target}) => setMinPlayers(target.value)}/>
      </div>
      <div>
        <TextField label="Description" value={description} onChange={({target}) => setDescription(target.value)} multiline/>
      </div>
      <MuiPickersUtilsProvider utils={MomentUtils}>
        <div>
          <DateTimePicker label="Start Time" value={startTime} onChange={setStartTime}/>
        </div>
        <div>
          <DateTimePicker label="End Time" value={endTime} onChange={setEndTime}/>
        </div>
      </MuiPickersUtilsProvider>

      {/*
      <div>
        <TextField label="Channel Id" type='number' value={channelId} onChange={({target}) => setChannelId(target.value)}/>
      </div>
      */}
      <Button variant='contained' color='primary' type='submit'>Create Party</Button>
    </form>
  )
}

export default PartyForm
