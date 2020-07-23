import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Button,
  Paper,
} from '@material-ui/core'

import partyService from '../services/parties'

const Parties = () => {
  const [ parties, setParties ] = useState([])

  useEffect(() => {
    partyService
      .getAll()
      .then(data => {
        setParties(data)
      })
  }, [])


  const padding = {
    padding: 5
  }

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
          {parties.map((party, i) =>
            <TableRow key={i}>
              <TableCell style={padding} >{party.title}</TableCell>
              <TableCell style={padding} >{party.game}</TableCell>
              <TableCell style={padding} >{`${party.members.length}`}</TableCell>
              <TableCell style={padding} >
                <Link to={`/parties/${party.id}`}>
                  <Button variant='contained' color='primary' type='button'>show</Button>
                </Link>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  )
}

export default Parties
