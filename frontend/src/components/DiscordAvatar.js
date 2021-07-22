import React from 'react';

import { makeStyles  } from '@material-ui/core/styles';
import {
  Avatar,
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  small: {
    width: theme.spacing(5),
    height: theme.spacing(5),
  },
  large: {
    width: theme.spacing(7),
    height: theme.spacing(7),
  },
  xxl: {
    width: theme.spacing(9),
    height: theme.spacing(9)
  }
}));

const DiscordAvatar = ({ user, size }) => {
  const classes = useStyles();

  if (user.icon) {
    return (<Avatar alt={user.name} src={`https://cdn.discordapp.com/avatars/${user.discordId}/${user.icon}`} className={classes[size]}/>);
  } else {
    return (<Avatar alt={user.name} src={`https://cdn.discordapp.com/embed/avatars/${parseInt(user.discriminator) % 5}.png`} className={classes[size]}/>);
  }
};

export default DiscordAvatar;
