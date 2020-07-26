import React, { useState, useEffect } from 'react'
import {
  BrowserRouter as Router,
  Switch, Route, Link
} from 'react-router-dom'
import {
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Button,
} from '@material-ui/core'

import ChannelForm from './components/ChannelForm'
import PartyForm from './components/party/PartyForm'
import Parties from './components/Parties'
import Party from './components/party/Party'
import User from './components/User'

import playerService from './services/users'

const getLoginUrl = () => {
  const params = [
    'client_id=718047907617439804',
    'redirect_uir=http%3A%2F%2Fapi.party.hellshade.fi%2Foauth2%2Fcallback',
    'response_type=code',
    'scope=identify%20guilds'
  ].join('&')

  return `https://discord.com/api/oauth2/authorize?${params}`
}

const getLogoutUrl = () => {
  return 'http://api.party.hellshade.fi/logout'
}

const App = () => {
  const [ user, setUser ] = useState(null)

  useEffect(() => {
    playerService
      .getUser()
      .then(res => setUser(res))
  }, [])

  const padding = {
    padding: 5
  }

  return (
    <Container>
      <Router basename="/#">
        <AppBar position='static'>
          <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu"></IconButton>
            <Button color='inherit' component={Link} to="/" style={padding}>Home</Button>
            <Button color='inherit' component={Link} to="/channels/create" style={padding}>New Channel</Button>
            <Button color='inherit' component={Link} to="/parties/create" style={padding}>New Party</Button>
            <Button color='inherit' component={Link} to="/parties" style={padding}>Parties</Button>
            { user ?
                <div>
                  <Button color='inherit' component={Link} to={`/players/${user.id}`} style={padding}>{user.name}</Button>
                  <Button color='inherit' component='a' href={ getLogoutUrl() } style={padding}>Logout</Button>
                </div> :
                <Button color='inherit' component='a' href={ getLoginUrl() } style={padding}>Login</Button>
            }
          </Toolbar>
        </AppBar>

        <Switch>
          <Route path="/channels/create">
            <ChannelForm />
          </Route>
          <Route path="/parties/create">
            <PartyForm />
          </Route>
          <Route path="/parties/:id">
            <Party />
          </Route>
          <Route path="/parties">
            <Parties />
          </Route>
          <Route path="/players/:id">
            <User />
          </Route>
          <Route path="/">
            <h1>Home Page</h1>
          </Route>
        </Switch>

      </Router>
    </Container>
  )
}

export default App
