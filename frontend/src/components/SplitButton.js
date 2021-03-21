import React, { useState, useRef } from 'react';
import {
  Grid,
  ButtonGroup,
  Button,
  Popper,
  Grow,
  Paper,
  MenuList,
  MenuItem,
  ClickAwayListener,
} from '@material-ui/core';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  root: {
    background: 'rgba(255,255,255,0.1)',
    backdropFilter: 'blur(40px)',
    border: 'solid 2px transparent',
  }
}));

const SplitButton = ({ options, selected, setSelected }) => {
  const classes = useStyles();

  const [open, setOpen] = useState(false);
  const anchorRef = useRef(null);

  const handleToggle = () => {
    setOpen(!open);
  };

  const handleClose = (event) => {
    if (anchorRef.current && anchorRef.current.contains(event.target)) {
      return;
    }

    setOpen(false);
  };

  const handleMenuItemClick = (event, index) => {
    setSelected(index);
    setOpen(false);
  };

  return (
    <Grid container>
      <Grid item>
        <ButtonGroup ref={anchorRef}>
          <Button onClick={handleToggle}>
            {options[selected]}
            <ArrowDropDownIcon />
          </Button>
        </ButtonGroup>
        <Popper open={open} anchorEl={anchorRef.current} role={undefined} transition>
          {({ TransitionProps, placement }) => (
            <Grow
              {...TransitionProps}
              style={{
                transformOrigin: placement === 'bottom' ? 'center top' : 'center bottom',
              }}
            >
              <Paper className={classes.root}>
                <ClickAwayListener onClickAway={handleClose}>
                  <MenuList id="split-button-menu">
                    {options.map((option, index) => (
                      <MenuItem
                        key={option}
                        selected={index === selected}
                        onClick={(event) => handleMenuItemClick(event, index)}
                      >
                        {option}
                      </MenuItem>
                    ))}
                  </MenuList>
                </ClickAwayListener>
              </Paper>
            </Grow>
          )}
        </Popper>
      </Grid>
    </Grid>
  );
};

export default SplitButton;
