import React, { useState, useEffect } from 'react'

import {
  Button,
  MenuItem,
} from '@material-ui/core'
import {
  MuiPickersUtilsProvider,
} from '@material-ui/pickers'
import MomentUtils from '@date-io/moment';

import { Formik, Form, Field } from 'formik';
import { TextField, Select } from 'formik-material-ui';
import { DateTimePicker } from 'formik-material-ui-pickers'

import partyService from '../../services/parties'
import channelService from '../../services/channels'

const initialChannels = [
  "none",
  "chess",
  "gw",
  "dotka",
]

const PartyForm = () => {
  const [ channels, setChannels ] = useState(null)

  useEffect(() => {
    setChannels(initialChannels)
    /*
     * Wait for backend to implement 'get all channels'
    channelService
      .getAll()
      .then(res => setChannels(res))
      */
  }, [])

  return (
    <MuiPickersUtilsProvider utils={MomentUtils}>
      <Formik
        initialValues={{
          title: '',
          leaderId: 2,
          channel: 'none',
          game: 'Dota 2',
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
          setTimeout(() => {
            setSubmitting(false);
            alert(JSON.stringify(values, null, 2));
          }, 500);
        }}
      >
        {({ submitForm, isSubmitting }) => (
          <Form>
            <Field component={TextField} name="title" label="Title" />
            <br />
            { channels &&
            <Field component={Select} name="channel" displayEmpty>
              { channels.map(channel => (
                <MenuItem value={channel} key={channel} >{channel}</MenuItem>
              ))
              }
            </Field>
            }
            <br />
            <Field component={TextField} name="leaderId" type="number" label="Leader Id" />
            <br />
            <Field component={TextField} name="game" label="Game" />
            <br />
            <Field component={TextField} name="maxPlayers" type="number" label="Max Players" />
            <br />
            <Field component={TextField} name="minPlayers" type="number" label="Min Players"
            />
            <br />
            <Field component={TextField} name="description" label="Description" />
            <br />
            <Field component={TextField} name="channelId" type="number" label="Channel Id" />
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

    </MuiPickersUtilsProvider>
  )
}

export default PartyForm
