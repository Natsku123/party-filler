import React, { useEffect, useState } from 'react';
import { Field } from 'formik';
import { partyService } from '../../services/parties';
import { gameService } from '../../services/games';
import { Button, Chip, Grid, IconButton, InputLabel, MenuItem, Select } from '@material-ui/core';
import { Skeleton } from '@material-ui/lab';

import CloseIcon from '@material-ui/icons/Close';


const PartySuggestedGames = ({ player, name }) => {
  const [ games, setGames ] = useState([]);
  const [ allGames, setAllGames ] = useState([]);
  const [ gamesReady, setGamesReady ] = useState(false);

  useEffect(() => {
    (async () => {
      await gameService.getAll().then(res => {
        setAllGames(res);
      });

      await partyService.getAll().then(res => {
        let gs = {};

        const promises = Object.entries(res.filter(p => p.members.some(m => m.playerId === player.id))
          .map(p => p.gameId)
          .reduce((c, e) => {
            if (!c[e]) c[e] = 1;
            else c[e]++;
            return c;
          },{}))
          .sort((a, b) => b[1] - a[1])
          .map((g, i) => {
            return gameService.getOne(g[0]).then(game => {
              if (!gs[i]) gs[i] = game;
            });
          });

        Promise.all(promises).then(() => {
          gs = Object.values(gs);

          if (gs.length < 5) {
            gs = gs.concat(allGames.filter(g => gs.findIndex(c => c.id === g.id) === -1));
          }
          setGames(gs.slice(0, gs.length < 5 ? gs.length : 5));
          setGamesReady(true);
        });
      });
    })();
  }, [player]);

  return (
    <Field name={ name } id={ name } type="number">
      {({ field: { value }, form: { setFieldValue } }) => (
        <Grid container spacing={1} alignItems={'center'}>
          <Grid item xs={12}>
            <label htmlFor={ name } className={'label-color'}>
              Suggested games
            </label>
          </Grid>
          { games && gamesReady ? games.map(g => <Grid item key={g.name + '-' + g.id}>
            <Chip label={g.name} color={value === g.id ? 'primary' : 'default'} onClick={() => setFieldValue(name, g.id)} />
          </Grid>) : <Skeleton variant={'rect'} /> }
          <Grid item>
            { gamesReady && allGames.filter(c => games.findIndex(g => g.id === c.id) === -1).length > 0
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
                  { allGames.filter(c => games.findIndex(g => g.id === c.id) === -1).map(game => (
                    <MenuItem value={game.id} key={game.id}>{game.name}</MenuItem>
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

export default PartySuggestedGames;
