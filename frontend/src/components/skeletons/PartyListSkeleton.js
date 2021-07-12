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
  TableRow, Typography
} from '@material-ui/core';

import { Link } from 'react-router-dom';
import { withStyles } from '@material-ui/core/styles';
import { Skeleton } from '@material-ui/lab';

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

const ShowButtonSkeleton = () => {
  return (
    <Skeleton variant='rect' height={40} width={90} />
  );
};

const TypographySkeleton = (props) => {
  const classes = useStyles();

  return (
    <Typography className={classes.bodyText} {...props}>
      <Skeleton />
    </Typography>
  );
};

export const PartyListSkeleton = ({ title }) => {
  const classes = useStyles();

  const padding = {
    padding: 5
  };

  // Skeleton array ('empty')
  const parties = [1, 2, 3, 4, 5];

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
                <TableCell className={classes.bodyText} style={padding}><TypographySkeleton /></TableCell>
                <TableCell className={classes.bodyText} style={padding}><TypographySkeleton /></TableCell>
                <TableCell className={classes.bodyText} style={padding}><TypographySkeleton /></TableCell>
                <TableCell className={classes.bodyText} style={padding}><TypographySkeleton /></TableCell>
                <TableCell className={classes.bodyText} style={padding}>
                  <ShowButtonSkeleton />
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};