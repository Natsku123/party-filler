import React from 'react';
import { makeStyles } from '@material-ui/core';

const useStyles = makeStyles(() => ({
  spacer: {
    flexGrow: 1,
  }
}));

export const Spacer = () => {
  const classes = useStyles();

  return <div className={classes.spacer} />;
};