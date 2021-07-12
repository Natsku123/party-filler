import React, { useState, useEffect } from 'react';

import { PartyListContainer } from './PartyListContainer';

import { PartyListSkeleton } from '../skeletons/PartyListSkeleton';

import { partyService } from '../../services/parties';

const Parties = (props) => {
  const [ parties, setParties ] = useState([]);
  const [ loading, setLoading ] = useState(true);

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


  return (
    <>
      { loading
        ? <PartyListSkeleton title={'Your active parties:'} />
        : <PartyListContainer parties={parties} title={'Your active parties:'} />
      }
    </>
  );
};

export default Parties;
