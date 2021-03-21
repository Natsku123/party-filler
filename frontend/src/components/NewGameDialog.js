import React, { useState } from 'react';

import {
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

import { gameService } from '../services/games';

const useStyles = makeStyles(() => ({
  root: {
    position: 'relative',
    backdropFilter: 'blur(40px)',
    backgroundClip: 'padding-box'
  },
  dialog: {
    backgroundColor: '#333333',
  },
}));

const NewGameDialog = ({ newGameDialog, closeNewGameDialog, onError, onSuccess }) => {
  const classes = useStyles();
  const [ newGameName, setNewGameName ] = useState('');
  const [ newGameSize, setNewGameSize ] = useState(5);

  const close = () => {
    closeNewGameDialog();
    setNewGameName('');
    setNewGameSize(5);
  };

  const createGame = (name, size) => {
    const newObject = {
      'name': name,
      'defaultMaxPlayers': size,
    };
    gameService.create(newObject).then(res => {
      onSuccess(`Game ${res.name} created.`);
    }, e => {
      onError(e.response.data.detail);
    });
    closeNewGameDialog();
  };

  return (
    <Dialog open={newGameDialog} onClose={close} aria-labelledby="form-dialog-title" className={classes.root}>
      <DialogTitle id="form-dialog-title" className={classes.dialog}>Create a new game</DialogTitle>
      <DialogContent className={classes.dialog}>
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
          onChange={({ target }) => setNewGameSize(target.value)}
          fullWidth
        />
      </DialogContent>
      <DialogActions className={classes.dialog}>
        <Button onClick={close} color="primary">
          Cancel
        </Button>
        <Button onClick={() => createGame(newGameName, newGameSize)} color="primary">
          Create
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default NewGameDialog;
