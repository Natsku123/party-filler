import React, { useEffect, useState } from 'react';
import {
  TextField,
  Button, DialogTitle, DialogContent, DialogContentText, DialogActions, Dialog,
} from '@material-ui/core';
import {
  DateTimePicker,
  MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import MomentUtils from '@date-io/moment';

import { partyService } from '../../services/parties';
import SplitButton from '../SplitButton';
import Glass from '../Glass';
import { gameService } from '../../services/games';

const PartyEdit = ({ party, setEdit, setParty, onError, onSuccess }) => {
  const [ title, setTitle ] = useState(party.title);
  const [ leaderId ] = useState(party.leaderId);
  const [ maxPlayers, setMaxPlayers ] = useState(party.maxPlayers);
  const [ minPlayers, setMinPlayers ] = useState(party.maxPlayers);
  const [ description, setDescription ] = useState(party.description);
  const [ startTime, setStartTime ] = useState(new Date());
  const [ endTime, setEndTime ] = useState(new Date(startTime.getTime() + (60*60*1000)));

  const [ games, setGames ] = useState(null);
  const [ gNames, setGNames ] = useState([]);
  const [ selectedGame, setSelectedGame ] = useState(0);
  const [ newGameDialog, setNewGameDialog ] = useState(false);

  const [ newGameName, setNewGameName ] = useState('');
  const [ newGameSize, setNewGameSize ] = useState(5);

  useEffect(() => {
    gameService.getAll().then(r => {
      let names = [];
      r.forEach(game => {
        names.push(game.name);
      });
      setGames(r);
      setGNames(names);
      setSelectedGame(r.findIndex(game => party.gameId === game.id));
    }, e => {
      onError(e.response.data.detail);
    });
  }, [onError, party.gameId]);

  const openNewGameDialog = () => {
    setNewGameDialog(true);
  };

  const closeNewGameDialog = () => {
    setNewGameDialog(false);
    setNewGameName('');
    setNewGameSize(5);
  };

  const changeGame = (game) => {
    setSelectedGame(game);
    const newCurrent = games[game];
    setMaxPlayers(newCurrent.defaultMaxPlayers);
    setMinPlayers(newCurrent.defaultMaxPlayers);
  };

  const createGame = () => {
    const newObject = {
      'name': newGameName,
      'defaultMaxPlayers': newGameSize
    };
    gameService.create(newObject).then(r => {
      onSuccess('Game ' + r.name + ' created.');
      const g = games;
      const gn = gNames;
      gn.push(r.name);
      g.push(r);
      setGames(g);
      setGNames(gn);
    }, e => {
      onError(e.response.data.detail);
    });
    closeNewGameDialog();
  };

  const editParty = (event) => {
    event.preventDefault();
    const newParty = {
      party: {
        title,
        leaderId,
        gameId: games[selectedGame].id,
        maxPlayers,
        minPlayers,
        description,
        startTime,
        endTime,
      }
    };

    partyService
      .update(party.id, newParty)
      .then(res => setParty(res));
    setEdit(false);
  };

  const cancel = (event) => {
    setEdit(false);
  };

  return (
    <div>
      <div>
        <TextField label="Title" value={title} onChange={({ target }) => setTitle(target.value)}/>
      </div>
      <div>
        { games ?
          <div>
                  game:
            <SplitButton options={gNames} selected={selectedGame} setSelected={changeGame}/>
          </div> :
          <div>loading games...</div>
        }
        <div>
          <Button variant="outlined" color="primary" onClick={openNewGameDialog}>New Game</Button>
        </div>
      </div>
      <div>
        <TextField label="Max Players" type='number' min='1' value={maxPlayers} onChange={({ target }) => setMaxPlayers(target.value)}/>
      </div>
      <div>
        <TextField label="Min Players" type='number' min='1' value={minPlayers} onChange={({ target }) => setMinPlayers(target.value)}/>
      </div>
      <div>
        <TextField label="Description" value={description} onChange={({ target }) => setDescription(target.value)} multiline/>
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
      <Button variant='contained' color='primary' onClick={editParty}>Save</Button>
      <Button variant='contained' color='secondary' onClick={cancel}>Cancel</Button>
      <Dialog open={newGameDialog} onClose={closeNewGameDialog} aria-labelledby="form-dialog-title">
        <DialogTitle id="form-dialog-title">Create a new game</DialogTitle>
        <DialogContent>
          <DialogContentText>
                    To create a new game, give the name of the game and a default party maximum party size
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="game-name"
            label="Name"
            value={newGameName}
            onChange={({ target }) => setNewGameName(target.value)}
            fullWidth
          />
          <TextField
            margin="dense"
            id="game-max-size"
            label="Max Party size"
            type="number"
            value={newGameSize}
            onChange={({ target }) => setNewGameSize(Number(target.value))}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={closeNewGameDialog} color="primary">
                    Cancel
          </Button>
          <Button onClick={createGame} color="primary">
                    Create
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default PartyEdit;
