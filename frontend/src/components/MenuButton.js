import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { Button } from '@material-ui/core';


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

export default MenuButton;