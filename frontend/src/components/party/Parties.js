import React, { useState, useEffect } from 'react';

import { PartyListContainer } from './PartyListContainer';

import { PartyListSkeleton } from '../skeletons/PartyListSkeleton';

import { partyService } from '../../services/parties';
import { playerService } from '../../services/players';
import { Grid } from '@material-ui/core';

const Parties = (props) => {
  const [ parties, setParties ] = useState([]);
  const [ loading, setLoading ] = useState(true);
  const [ player, setPlayer ] = useState(null);

  useEffect(() => {
    partyService
      .getAll()
      .then(data => {
        setParties(data);
        setLoading(false);
      }).catch(error => {
        props.onError(error.response.data.detail);
      });
  }, [props]);

  useEffect(() => {
    playerService.getCurrent().then(data => {
      setPlayer(data);
    }).catch(error => {
      console.log(error);
    });
  }, [props]);


  return (
    <Grid container spacing={4}>
      <Grid item xs={12}>
        { player && <>
          { loading
            ? <PartyListSkeleton title={'Your active parties:'} />
            : <PartyListContainer parties={parties.filter(p => p.members.findIndex(m => m.playerId === player.id) !== -1).filter(p => new Date(p.endTime) > new Date())} title={'Your active parties:'} />}
        </>}
      </Grid>
      <Grid item xs={12}>
        { loading
          ? <PartyListSkeleton title={'New parties:'} />
          : <PartyListContainer parties={parties.filter(p => new Date(p.endTime) > new Date())} title={'New parties:'} buttonColor={'#A4D555'} />}
      </Grid>
      <Grid item xs={12}>
        { loading
          ? <PartyListSkeleton title={'Old parties:'} />
          : <PartyListContainer parties={parties.filter(p => new Date(p.endTime) <= new Date())} title={'Old parties:'} />}
      </Grid>
    </Grid>
  );
};

export default Parties;
