import React, { useState, useEffect } from 'react';

import {
  Button, Grid, IconButton,
  Typography,
} from '@material-ui/core';
import {
  MuiPickersUtilsProvider,
} from '@material-ui/pickers';
import MomentUtils from '@date-io/moment';

import { Formik, Form, Field } from 'formik';
import { TextField } from 'formik-material-ui';
import { DateTimePicker } from 'formik-material-ui-pickers';

import { partyService } from '../../services/parties';
import { playerService } from '../../services/players';

import NewGameDialog from '../NewGameDialog';
import { Skeleton } from '@material-ui/lab';
import { makeStyles, withStyles } from '@material-ui/core/styles';

import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import PartySuggestedGames from './PartySuggestedGames';
import { useHistory } from 'react-router-dom';
import PartySuggestedChannels from './PartySuggestedChannels';

const useStyles = makeStyles(() => ({
  form: {
    width: '100%'
  }
}));

const PageTitle = withStyles({
  root: {
    fontFamily: 'Montserrat',
    fontSize: '20px',
    fontStyle: 'normal',
    fontWeight: 400,
    lineHeight: '41px',
    letterSpacing: '0em',
    textAlign: 'center',
    padding: 5,
    border: '1px solid #88B8D6',
  }
})(Typography);

const PartyCreate = (props) => {
  const classes = useStyles();

  const [ currentUser, setCurrentUser ] = useState(null);

  const [ newGameDialog, setNewGameDialog ] = useState(false);

  const [ playerReady, setPlayerReady ] = useState(false);

  const history = useHistory();

  useEffect(() => {
    playerService.getCurrent().then(res => {
      setCurrentUser(res);
      setPlayerReady(true);
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

  const openNewChannelDialog = () => {
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
    // TODO replace notify=true with selection box thingy
    partyService.create(partyObject, true).then(r => {
      props.onSuccess(`Party ${r.title} created.`);
    }).catch(e => {
      const eMsg = Array.isArray(e.response.data.detail) ? e.response.data.detail.reduce((msg, c) => {
        return msg + '\n' + c.msg;
      }, '') : e.response.data.detail;
      props.onError(eMsg);
    }).finally(() => {
      setSubmitting(false);
    });
  };

  const cancelForm = () => {
    history.goBack();
  };

  return (
    <>
      <Grid container>
        <Grid item xs={6}>
          <Grid container spacing={2} alignItems={'center'}>
            <Grid item xs={1}>
              <IconButton onClick={cancelForm}><ArrowBackIcon /></IconButton>
            </Grid>
            <Grid item xs={4}>
              <PageTitle>
                Create a new party
              </PageTitle>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
      <MuiPickersUtilsProvider utils={MomentUtils}>
        <Formik
          initialValues={initialFormValues}
          onSubmit={submitForm}
          className={classes.form}
        >
          {({ submitForm, isSubmitting }) => (
            <Form>
              <Grid container spacing={2} alignItems={'center'}>
                <Grid item xs={5}>
                  <Field component={TextField} fullWidth name="title" label="Title" validate={validateString} />
                </Grid>
                <Grid item xs={7} />
                <Grid item xs={9}>
                  <Grid container spacing={2} alignItems={'center'}>
                    <Grid item xs>
                      { playerReady ? <PartySuggestedGames player={currentUser} name="gameId"/> : <Skeleton variant={'rect'} /> }
                    </Grid>
                    <Grid item xs>
                      <Button variant="outlined" color="primary" onClick={openNewGameDialog}>New Game</Button>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={2}/>
                <Grid item xs={9}>
                  <Grid container spacing={2} alignItems={'center'}>
                    <Grid item xs>
                      { playerReady ? <PartySuggestedChannels player={currentUser} name="channelId"/> : <Skeleton variant={'rect'} /> }
                    </Grid>
                    <Grid item xs>
                      <Button variant="outlined" color="primary" onClick={openNewChannelDialog}>New Channel</Button>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={3} />
                <Grid item xs={3}>
                  <Field component={TextField} fullWidth name="minPlayers" type="number" label="Min Players" />
                </Grid>
                <Grid item xs={3}>
                  <Field component={TextField} fullWidth name="maxPlayers" type="number" label="Max Players" />
                </Grid>
                <Grid item xs={12}>
                  <Field component={TextField} fullWidth multiline rows={4} name="description" label="Description" validate={validateString} />
                </Grid>
                <Grid item xs={3}>
                  <Field component={DateTimePicker} fullWidth label="Start Time" name="startTime" />
                </Grid>
                <Grid item xs={3}>
                  <Field component={DateTimePicker} fullWidth label="End Time" name="endTime" />
                </Grid>
                <Grid item xs={6} />
                <Grid item xs={12}>
                  <Grid container justify={'space-between'}>
                    <Grid item xs={2}>
                      <Button
                        variant="contained"
                        color="green"
                        disabled={isSubmitting}
                        onClick={submitForm}
                      >
                        Create Party
                      </Button>
                    </Grid>
                    <Grid item xs={1}>
                      <Button
                        variant="contained"
                        color="red"
                        disabled={isSubmitting}
                        onClick={cancelForm}
                      >
                        Cancel
                      </Button>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
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
    </>
  );
};

export default PartyCreate;
