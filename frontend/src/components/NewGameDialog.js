import React from 'react';

import {
  Button,
  MenuItem,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField as TF
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

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

const NewGameDialog = (props) => {
  const {
    newGameDialog,
    closeNewGameDialog,
    newGameName,
    setNewGameName,
    newGameSize,
    setNewGameSize,
    createGame
  } = props;
  const classes = useStyles();

  return (
    <Dialog open={newGameDialog} onClose={closeNewGameDialog} aria-labelledby="form-dialog-title" className={classes.root}>
      <DialogTitle id="form-dialog-title" className={classes.dialog}>Create a new game</DialogTitle>
      <DialogContent className={classes.dialog}>
        <DialogContentText>
          To create a new game, give the name of the game and a default party maximum party size
        </DialogContentText>
        <TF
          autoFocus
          margin="dense"
          id="game-name"
          label="Name"
          value={newGameName}
          onChange={({ target }) => setNewGameName(target.value)}
          fullWidth
        />
        <TF
          margin="dense"
          id="game-max-size"
          label="Max Party size"
          type="number"
          value={newGameSize}
          onChange={({ target }) => setNewGameSize(Number(target.value))}
          fullWidth
        />
      </DialogContent>
      <DialogActions className={classes.dialog}>
        <Button onClick={closeNewGameDialog} color="primary">
          Cancel
        </Button>
        <Button onClick={createGame} color="primary">
          Create
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default NewGameDialog;
