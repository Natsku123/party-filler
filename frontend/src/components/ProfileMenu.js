import React, { useEffect, useRef, useState } from 'react';
import { Grid, Menu, MenuItem, Typography } from '@material-ui/core';
import DiscordAvatar from './DiscordAvatar';
import { NavLink } from 'react-router-dom';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import MenuButton from './MenuButton';

const baseUrl = '/api';

const getLogoutUrl = () => {
  return `${baseUrl}/logout`;
};


const useStyles = makeStyles(() => ({
  link: {
    padding: 5,
  },
  profileMenuLink: {
    paddingLeft: 10,
    paddingRight: 10,
    width: '100%'
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
  }
}));


const ProfileMenu = ({ user }) => {
  const classes = useStyles();

  const [anchorEl, setAnchorEl] = React.useState(null);
  const profileButtonRef = useRef(null);
  const [buttonW, setButtonW] = useState(150);

  const ProfileMenuEl = withStyles({
    paper: {
      border: '1px solid #4F4F4F',
      borderRadius: 0,
      width: buttonW
    },
  })((props) => (
    <Menu
      elevation={0}
      getContentAnchorEl={null}
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'center',
      }}
      transformOrigin={{
        vertical: 'top',
        horizontal: 'center',
      }}
      autoFocus={false}
      {...props}
    />
  ));

  const ProfileMenuItem = withStyles((theme) => ({
    root: {
      '&:focus': {
        backgroundColor: theme.palette.primary.main, '& .MuiListItemIcon-root, & .MuiListItemText-primary': {
          color: theme.palette.common.white,
        },
      }
    },
  }))(MenuItem);

  const ProfileMenuText = withStyles({
    root: {
      fontFamily: 'Montserrat',
      fontSize: '20px',
      fontStyle: 'normal',
      fontWeight: 400,
      lineHeight: '30px',
      letterSpacing: '0em',
      textAlign: 'center',
      textDecoration: 'none',
      boxShadow: 'none',
      color: 'black'
    }
  })(Typography);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  useEffect(() => {
    if (profileButtonRef.current) {
      setButtonW(profileButtonRef.current.offsetWidth);
    }
  }, [profileButtonRef.current]);

  return (
    <>
      <MenuButton ref={profileButtonRef} aria-controls="customized-menu" aria-haspopup="true" onClick={handleClick} activeClassName={classes.activeLink} className={classes.link}>
        <Grid container spacing={1} alignItems="center">
          <Grid item>
            <DiscordAvatar user={user} size='medium' className={classes.avatar} />
          </Grid>
          <Grid item>
            {user.name}
          </Grid>
        </Grid>
      </MenuButton>
      <ProfileMenuEl id="profile-menu" anchorEl={anchorEl} keepMounted open={Boolean(anchorEl)} onClose={handleClose}>
        <ProfileMenuItem disableGutters>
          <ProfileMenuText component={NavLink} exact to="/profile" activeClassName={classes.activeLink} className={classes.profileMenuLink} onClick={handleClose}>My profile</ProfileMenuText>
        </ProfileMenuItem>
        <ProfileMenuItem disableGutters>
          <ProfileMenuText component={NavLink} exact to="/profile/settings" activeClassName={classes.activeLink} className={classes.profileMenuLink} onClick={handleClose}>Settings</ProfileMenuText>
        </ProfileMenuItem>
        <ProfileMenuItem disableGutters>
          <ProfileMenuText component='a' href={ getLogoutUrl() } className={classes.profileMenuLink} onClick={handleClose}>Logout</ProfileMenuText>
        </ProfileMenuItem>
      </ProfileMenuEl>
    </>
  );
};

export default ProfileMenu;
