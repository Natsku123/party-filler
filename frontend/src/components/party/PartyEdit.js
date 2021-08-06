import React, { useEffect, useState } from 'react';
import {
  Button,
  MenuItem,
} from '@material-ui/core';
import {
  MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import MomentUtils from '@date-io/moment';

import { Formik, Form, Field } from 'formik';
import { TextField, Select } from 'formik-material-ui';
import { DateTimePicker } from 'formik-material-ui-pickers';

import { partyService } from '../../services/parties';
import { playerService } from '../../services/players';
import { gameService } from '../../services/games';

import NewGameDialog from '../NewGameDialog';

const PartyEdit = ({ party, setEdit, onError, onSuccess }) => {
  const [ channels, setChannels ] = useState(null);
  const [ games, setGames ] = useState(null);

  const [ newGameDialog, setNewGameDialog ] = useState(false);

  useEffect(() => {
    playerService.getVisibleChannels().then(res => {
      setChannels(res);
    }).catch(e => {
      onError(e.response.data.detail);
    });

    gameService.getAll().then(res => {
      setGames(res);
    }).catch(e => {
      onError(e.response.data.detail);
    });
  }, [onError, party.gameId]);

  const openNewGameDialog = () => {
    setNewGameDialog(true);
  };

  const closeNewGameDialog = () => {
    setNewGameDialog(false);
  };

  if (channels === null || games === null) {
    return (<div>Loading...</div>);
  }

  const {
    title,
    channelId,
    leaderId,
    gameId,
    maxPlayers,
    minPlayers,
    description,
    startTime,
    endTime,
  } = party;

  const initialFormValues = {
    title,
    channelId,
    leaderId,
    gameId,
    maxPlayers,
    minPlayers,
    description,
    startTime,
    endTime,
  };

  const validateString = value => {
    let error;
    if (!value) {
      error = 'Required';
    } else if (value.length < 3) {
      error = 'Too short! (Minimum 3 characters)';
    }
    return error;
  };

  const submitForm = (values, { setSubmitting }) => {
    const partyObject = {
      ...values
    };
    partyService.create(partyObject).then(r => {
      onSuccess(`Party ${r.title} updated.`);
    }).catch(e => {
      onError(e.response.data.detail);
    }).finally(() => {
      setSubmitting(false);
      setEdit(false);
    });
  };

  return (
    <MuiPickersUtilsProvider utils={MomentUtils}>
      <Formik
        initialValues={initialFormValues}
        onSubmit={submitForm}
      >
        {({ submitForm, isSubmitting }) => (
          <Form>
            <Field component={TextField} name="title" label="Title" validate={validateString} />
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
            <Field component={TextField} name="description" label="Description" validate={validateString} />
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
          </Form>
        )}
      </Formik>
      <NewGameDialog
        newGameDialog={newGameDialog}
        closeNewGameDialog={closeNewGameDialog}
        onError={onError}
        onSuccess={onSuccess}
      />
    </MuiPickersUtilsProvider>
  );
};

export default PartyEdit;
