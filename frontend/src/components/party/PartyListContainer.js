import React from 'react';
import {
  Button,
  makeStyles,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@material-ui/core';

import { Link } from 'react-router-dom';
import { withStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
  root: {
    backgroundColor: '#F0F0F0',
    paddingLeft: 20,
    paddingRight: 20,
    paddingTop: 5,
    paddingBottom: 5,
  },
  title: {
    backgroundColor: '#E4E4E4',
    fontFamily: 'Montserrat',
    fontSize: '25px',
    fontStyle: 'normal',
    fontWeight: '400',
    lineHeight: '30px',
    letterSpacing: '0em',
    textAlign: 'left',
    padding: 5,
    borderBottomStyle: 'solid',
    borderBottomWidth: 3,
    borderBottomColor: '#43B581'
  },
  header: {
    backgroundColor: '#E4E4E4'
  },
  headerText: {
    fontFamily: 'Montserrat',
    fontSize: '20px',
    fontStyle: 'normal',
    fontWeight: '400',
    lineHeight: '23px',
    letterSpacing: '0em',
    textAlign: 'left',
  },
  bodyText: {
    fontFamily: 'Montserrat',
    fontSize: '15px',
    fontStyle: 'normal',
    fontWeight: '400',
    lineHeight: '28px',
    letterSpacing: '0em',
    textAlign: 'left',
  }
}));

const dateFormat = (date) => {
  const parsed = new Date(date);
  const a = parsed.toTimeString().split(':');
  a.pop();
  return `${a.join(':')} ${parsed.toLocaleDateString()}`;
};

const ShowButton = withStyles({
  root: {
    backgroundColor: '#88B8D6',
    borderRadius: '0px',
    height: '20px',
    fontFamily: 'Montserrat',
    fontSize: '15px',
    fontStyle: 'normal',
    fontWeight: '400',
    lineHeight: '30px',
    letterSpacing: '0em',
    textAlign: 'center',
    padding: '20px'
  }
})(Button);

export const PartyListContainer = ({ parties, title }) => {
  const classes = useStyles();

  const padding = {
    padding: 5
  };

  return (
    <div className={classes.root}>
      <div className={classes.title}>{title}</div>
      <TableContainer>
        <Table>
          <TableHead className={classes.header}>
            <TableRow>
              <TableCell className={classes.headerText} style={padding}>Title</TableCell>
              <TableCell className={classes.headerText} style={padding}>Game</TableCell>
              <TableCell className={classes.headerText} style={padding}>Members</TableCell>
              <TableCell className={classes.headerText} style={padding}>End Time</TableCell>
              <TableCell className={classes.headerText} style={padding}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {parties.map((party, i) =>
              <TableRow key={i}>
                <TableCell className={classes.bodyText} style={padding}>{party.title}</TableCell>
                <TableCell className={classes.bodyText} style={padding}>{party.game.name}</TableCell>
                <TableCell className={classes.bodyText} style={padding}>{`${party.members.length}`}</TableCell>
                <TableCell className={classes.bodyText} style={padding}>{dateFormat(party.endTime)}</TableCell>
                <TableCell className={classes.bodyText} style={padding}>
                  <ShowButton component={Link} to={`/parties/${party.id}`} variant='contained' type='button'>show</ShowButton>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};