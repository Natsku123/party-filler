import React, { useState, useEffect } from 'react'

import {
  Button,
  MenuItem,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField as TF
} from '@material-ui/core'
import {
  MuiPickersUtilsProvider,
} from '@material-ui/pickers'
import MomentUtils from '@date-io/moment';

import { Formik, Form, Field } from 'formik';
import { TextField, Select } from 'formik-material-ui';
import { DateTimePicker } from 'formik-material-ui-pickers'

import { partyService } from '../../services/parties'
import { playerService } from "../../services/players";
import { serverService } from "../../services/servers";
import {gameService} from "../../services/games";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    root: {
        position: "relative",
        backdropFilter: "blur(40px)",
        backgroundClip: "padding-box"
    },
    dialog: {
        backgroundColor: "#333333"
    }
}))

const PartyForm = (props) => {
  const classes = useStyles();
  const [ channels, setChannels ] = useState([])
  const [ currentUser, setCurrentUser ] = useState(null);
  const [ games, setGames ] = useState(null);
  const [ gNames, setGNames ] = useState(null);

  const [ newGameDialog, setNewGameDialog ] = useState(false);

  const [ newGameName, setNewGameName ] = useState("");
  const [ newGameSize, setNewGameSize ] = useState(5);

  useEffect(() => {
      playerService.getCurrent().then(r => {
          setCurrentUser(r);
      }, e => {
          props.onError(e.response.data.detail);
      });

      playerService.getVisibleChannels().then(r => {
          setChannels(r);
      }, e => {
          props.onError(e.response.data.detail);
      });
  }, [props])

  useEffect(() => {
      gameService.getAll().then(r => {
          const names  = r.map(game => game.name);
          setGames(r);
          setGNames(names);
      }, e => {
          props.onError(e.response.data.detail);
      });
  }, [props])

  const openNewGameDialog = () => {
    setNewGameDialog(true);
  }

  const closeNewGameDialog = () => {
    setNewGameDialog(false);
    setNewGameName("");
    setNewGameSize(5);
  }

  const createGame = () => {
    const newObject = {
        "name": newGameName,
        "defaultMaxPlayers": newGameSize
    };
    gameService.create(newObject).then(r => {
        props.onSuccess("Game " + r.name + " created.")
        const g = games;
        const gn = gNames;
        gn.push(r.name);
        g.push(r);
        setGames(g);
        setGNames(gn);
    }, e => {
        props.onError(e.response.data.detail)
    });
    closeNewGameDialog();
  }

  return (
    <MuiPickersUtilsProvider utils={MomentUtils}>
      <Formik
        initialValues={{
          title: '',
          channelId: '',
          gameId: '',
          maxPlayers: 5,
          minPlayers: 5,
          description: '',
          startTime: new Date(),
          endTime: new Date(),
        }}
        validate={values => {
          const errors = {}
          if (!values.title) {
            errors.title = 'Required';
          }
          return errors;
        }}
        onSubmit={(values, { setSubmitting }) => {
          const partyObject = {
            leaderId: currentUser.id,
            ...values
          }
          partyService.create(partyObject).then(r => {
              props.onSuccess("Party " + r.title + " created.");
            }, e => {
              props.onError(e.response.data.detail);
          }).finally(() => {
            setSubmitting(false);
          });
        }}
      >
        {({ submitForm, isSubmitting }) => (
          <Form>
            <Field component={TextField} name="title" label="Title" />
            <br />
            { channels &&
            <Field component={Select} name="channelId" label="Channel">
              { channels.map(channel => (
                <MenuItem value={channel.id} key={channel.id} >{channel.server.name} - {channel.name}</MenuItem>
              ))
              }
            </Field>
            }
            <br />
            {games &&
            <Field component={Select} name="gameId" label="Game">
              {games.map(game => (
                <MenuItem value={game.id} key={game.id}>{game.name}</MenuItem>
              ))
              }
            </Field>
            }
            <br />
            <Button variant="outlined" color="primary" onClick={openNewGameDialog}>New Game</Button>
            <br />
            <Field component={TextField} name="maxPlayers" type="number" label="Max Players" />
            <br />
            <Field component={TextField} name="minPlayers" type="number" label="Min Players"
            />
            <br />
            <Field component={TextField} name="description" label="Description" />
            <br />
            <Field component={DateTimePicker} label="Start Time" name="startTime" />;
            <br />
            <Field component={DateTimePicker} label="End Time" name="endTime" />;
            <br />
            <Button
              variant="contained"
              color="primary"
              disabled={isSubmitting}
              onClick={submitForm}
            >
              Create Party
            </Button>
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
                  onChange={({target}) => setNewGameName(target.value)}
                  fullWidth
                />
                <TF
                  margin="dense"
                  id="game-max-size"
                  label="Max Party size"
                  type="number"
                  value={newGameSize}
                  onChange={({target}) => setNewGameSize(Number(target.value))}
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
          </Form>
        )}
      </Formik>
    </MuiPickersUtilsProvider>
  )
}

export default PartyForm
