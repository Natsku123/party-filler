import React, { useEffect, useState } from 'react';
import { Field } from 'formik';
import { partyService } from '../../services/parties';
import { channelService } from '../../services/channels';
import { Button, Chip, Grid, IconButton, InputLabel, MenuItem, Select } from '@material-ui/core';
import { Skeleton } from '@material-ui/lab';

import CloseIcon from '@material-ui/icons/Close';


const PartySuggestedChannels = ({ player, name }) => {
  const [ channels, setChannels ] = useState([]);
  const [ allChannels, setAllChannels ] = useState([]);
  const [ channelsReady, setChannelsReady ] = useState(false);

  useEffect(() => {
    channelService.getAll().then(res => {
      if (player.servers) {
        setAllChannels(res.filter(c => player.servers.findIndex(s => s.id === c.id) !== -1));
      }
    });
  },[player]);

  useEffect(() => {
    partyService.getAll().then(res => {
      let gs = [];

      const promises = res.filter(p => p.members.some(m => m.playerId === player.id)).filter(p => p.channelId !== null).map(p => p.channelId).map(g => {
        return channelService.getOne(g).then(channel => {
          if (gs.findIndex(c => c.id === channel.id) === -1) gs.push(channel);
        });
      });

      Promise.all(promises).then(() => {
        if (gs.length < 5) {
          gs = gs.concat(allChannels.filter(g => gs.findIndex(c => c.id === g.id) === -1));
        }
        setChannels(gs.slice(0, gs.length < 5 ? gs.length : 5));
        setChannelsReady(true);
      });
    });
  }, [player, allChannels]);

  return (
    <Field name={ name } id={ name } type="number">
      {({ field: { value }, form: { setFieldValue } }) => (
        <Grid container spacing={1} alignItems={'center'}>
          <Grid item xs={12}>
            <label htmlFor={ name } className={'label-color'}>
              Suggested channels
            </label>
          </Grid>
          { channels && channelsReady ? channels.map(g => <Grid item key={g.name + '-' + g.id}>
            <Chip label={g.name} color={value === g.id ? 'primary' : 'default'} onClick={() => setFieldValue(name, g.id)} />
          </Grid>) : <Skeleton variant={'rect'} /> }
          <Grid item>
            { channelsReady && allChannels.filter(c => channels.findIndex(g => g.id === c.id) === -1).length > 0
              ? <>
                <InputLabel id="selectLabel">Other</InputLabel>
                <Select fullWidth labelId="selectLabel" id="select" value={''} onChange={(event) => {
                  if (event.target.value !== '') {
                    setFieldValue(name, event.target.value);
                  } else {
                    setFieldValue(name, null);
                  }
                }}>
                  <MenuItem value={''}>
                    <em>None</em>
                  </MenuItem>
                  { allChannels.filter(c => channels.findIndex(g => g.id === c.id) === -1).map(channel => (
                    <MenuItem value={channel.id} key={channel.id}>{channel.name}</MenuItem>
                  ))}
                </Select>
              </>
              : <></>
            }
          </Grid>
          <Grid item>
            <IconButton onClick={() => setFieldValue(name, null)}><CloseIcon /></IconButton>
          </Grid>
        </Grid>
      )}
    </Field>
  );
};

export default PartySuggestedChannels;
