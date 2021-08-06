import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { playerService } from '../services/players';
import DiscordAvatar from '../components/DiscordAvatar';


const Player = (props) => {
  const id = useParams().id;
  const [ user, setUser ] = useState(null);

  useEffect(() => {
    playerService.getOne(id).then(res => setUser(res))
      .catch(error =>
        props.onError(error.response.data.detail)
      );
  }, [ props, id ]);

  if (!user) {
    return <div>loading...</div>;
  }

  return (
    <div>
      <DiscordAvatar user={user} size='large' />
      <br />
      {user.name}
    </div>
  );
};

export default Player;
