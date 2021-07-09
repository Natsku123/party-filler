import React, { useState, useEffect } from 'react';

import { PartyListContainer } from './PartyListContainer';

import { partyService } from '../../services/parties';

const Parties = (props) => {
  const [ parties, setParties ] = useState([]);

  useEffect(() => {
    partyService
      .getAll()
      .then(data => {
        setParties(data);
      }).catch(error => {
        props.onError(error.response.data.detail);
      });
  }, [props]);




  return (
    <PartyListContainer parties={parties} title={'Your active parties:'} />
  );
};

export default Parties;
