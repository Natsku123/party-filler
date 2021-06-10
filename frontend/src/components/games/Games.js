import React, { useState, useEffect } from 'react';

import { Link } from 'react-router-dom';

import {
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Button,
  Paper,
} from '@material-ui/core';

import { gameService } from '../../services/games';

const Games = (props) => {
  const [ games, setGames ] = useState([]);

  useEffect(() => {
    gameService
      .getAll()
      .then(data => {
        setGames(data);
      }).catch(error => {
        props.onError(error.response.data.detail);
      });
  }, [props]);


  const padding = {
    padding: 5
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell>Game</TableCell>
            <TableCell>Members</TableCell>
            <TableCell />
          </TableRow>
        </TableHead>
        <TableBody>
          {games.map((game, i) =>
            <TableRow key={i}>
              <TableCell style={padding} >{game.name}</TableCell>
              <TableCell style={padding} >{game.defaultMaxPlayers}</TableCell>
              <TableCell style={padding} >
                <Link to={'/'}>
                  <Button variant='contained' color='secondary' type='button'>delete</Button>
                </Link>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Games;
