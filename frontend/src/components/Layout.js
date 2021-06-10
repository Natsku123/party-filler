import React, { useState, useEffect } from 'react';

import { Link } from 'react-router-dom';

import {
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Button,
  Grid,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';


const baseUrl = '/api';

const getLoginUrl = () => {
  return `${baseUrl}/login`;
};

const getLogoutUrl = () => {
  return `${baseUrl}/logout`;
};


const useStyles = makeStyles(() => ({
  link: {
    padding: 5,
  },
  grow: {
    flex: '1 1 auto',
  },
}));

const Layout = ({ user, children }) => {
  const classes = useStyles();

  return (
    <div>
      <AppBar position='static'>
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu"/>
          <Button color='inherit' component={Link} to="/" className={classes.link}>Home</Button>
          <Button color='inherit' component={Link} to="/channels/create" className={classes.link}>New Channel</Button>
          <Button color='inherit' component={Link} to="/parties/create" className={classes.link}>New Party</Button>
          <Button color='inherit' component={Link} to="/parties" className={classes.link}>Parties</Button>
          { user ?
            <div>
              <Button color='inherit' component={Link} to={'/games'} className={classes.link}>Games</Button>
              <Button color='inherit' component={Link} to={`/players/${user.id}`} className={classes.link}>{user.name}</Button>
              <Button color='inherit' component='a' href={ getLogoutUrl() } className={classes.link}>Logout</Button>
            </div> :
            <Button color='inherit' component='a' href={ getLoginUrl() } className={classes.link}>Login</Button>
          }
        </Toolbar>
      </AppBar>

      {children}
    </div>
  );
};

export default Layout;
