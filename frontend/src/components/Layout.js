import React, { useState, useEffect } from 'react';

import { NavLink } from 'react-router-dom';

import {
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Button,
  Grid, Typography,
} from '@material-ui/core';
import { makeStyles, withStyles } from '@material-ui/core/styles';

import { playerService } from '../services/players';
import DiscordAvatar from '../components/DiscordAvatar';

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
  activeLink: {
    fontWeight: '700!important'
  },
  links: {
    paddingTop: 10,
    paddingBottom: 10,
  },
  avatar: {
    marginRight: 10
  },
  grow: {
    flex: '1 1 auto',
  },
}));

const Title = withStyles({
  root: {
    fontFamily: 'Montserrat Subrayada',
    fontSize: '34px',
    fontStyle: 'normal',
    fontWeight: '400',
    lineHeight: '41px',
    letterSpacing: '0em',
    textAlign: 'center',
    textDecoration: 'none',
    boxShadow: 'none',
    color: 'white'
  }
})(Typography);


const MenuButton = withStyles({
  root: {
    backgroundColor: 'rgba(255, 255, 255, 0.5)',
    borderRadius: '0px',
    height: '58px',
    fontFamily: 'Montserrat',
    fontSize: '20px',
    fontStyle: 'normal',
    fontWeight: '400',
    lineHeight: '30px',
    letterSpacing: '0em',
    textAlign: 'center',
    padding: '20px'
  }
})(Button);

const Layout = ({ children }) => {
  const classes = useStyles();
  const [ user, setUser ] = useState(null);

  useEffect(() => {
    playerService
      .getCurrent()
      .then(res => setUser(res));
  }, []);

  return (
    <div>
      <AppBar position='static'>
        <Toolbar>
          <Grid container alignItems="center" className={classes.links}>
            <Grid item>
              <Title component={NavLink} to="/">PartyFiller</Title>
            </Grid>
            <Grid item xs />
            <Grid item>
              <Grid container spacing={1}>
                <Grid item>
                  <MenuButton component={NavLink} exact to="/parties" activeClassName={classes.activeLink} className={classes.link}>Parties</MenuButton>
                </Grid>
                <Grid item>
                  <MenuButton component={NavLink} exact to="/parties/create" activeClassName={classes.activeLink} className={classes.link}>New Party</MenuButton>
                </Grid>
                <Grid item>
                  <MenuButton component={NavLink} to="/about" activeClassName={classes.activeLink} className={classes.link}>About us</MenuButton>
                </Grid>
                { user ?
                  <>
                    <Grid item>
                      <MenuButton component={NavLink} to={`/players/${user.id}`} activeClassName={classes.activeLink} className={classes.link}>
                        <Grid container spacing={1} alignItems="center">
                          <Grid item>
                            <DiscordAvatar user={user} size='medium' className={classes.avatar} />
                          </Grid>
                          <Grid item>
                            {user.name}
                          </Grid>
                        </Grid>
                      </MenuButton>
                    </Grid>
                  </>:
                  <Grid item>
                    <MenuButton component='a' href={ getLoginUrl() } className={classes.link}>Login</MenuButton>
                  </Grid>
                }
              </Grid>
            </Grid>
          </Grid>

        </Toolbar>
      </AppBar>

      {children}
    </div>
  );
};

export default Layout;
