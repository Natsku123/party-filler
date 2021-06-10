import React, { useState, useEffect } from 'react';

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

const PartyForm = (props) => {
  const [ channels, setChannels ] = useState([]);
  const [ currentUser, setCurrentUser ] = useState(null);
  const [ games, setGames ] = useState([]);

  const [ newGameDialog, setNewGameDialog ] = useState(false);

  useEffect(() => {
    playerService.getCurrent().then(res => {
      setCurrentUser(res);
    }).catch(e => {
      props.onError(e.response.data.detail);
    });

    playerService.getVisibleChannels().then(res => {
      setChannels(res);
    }).catch(e => {
      props.onError(e.response.data.detail);
    });

    gameService.getAll().then(res => {
      setGames(res);
    }).catch(e => {
      props.onError(e.response.data.detail);
    });
  }, [props, newGameDialog]);

  const openNewGameDialog = () => {
    setNewGameDialog(true);
  };

  const closeNewGameDialog = () => {
    setNewGameDialog(false);
  };


  const initialFormValues = {
    title: '',
    channelId: '',
    gameId: '',
    maxPlayers: 5,
    minPlayers: 5,
    description: '',
    startTime: new Date(),
    endTime: new Date(),
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
      leaderId: currentUser.id,
      ...values
    };
    partyService.create(partyObject).then(r => {
      props.onSuccess(`Party ${r.title} created.`);
    }).catch(e => {
      props.onError(e.response.data.detail);
    }).finally(() => {
      setSubmitting(false);
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
        onError={props.onError}
        onSuccess={props.onSuccess}
      />
    </MuiPickersUtilsProvider>
  );
};

export default PartyForm;
