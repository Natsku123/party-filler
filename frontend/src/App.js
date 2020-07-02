import React, { useState, useEffect } from 'react'
import {
  BrowserRouter as Router,
  Switch, Route, Link
} from "react-router-dom"

import PartyForm from './components/PartyForm'
import Parties from './components/Parties'
import Party from './components/Party'
import User from './components/User'

import playerService from './services/players'

const getUrl = () => {
  const params = [
    'client_id=718047907617439804',
    'redirect_uir=http%3A%2F%2Fapi.party.hellshade.fi%2Foauth2%2Fcallback',
    'response_type=code',
    'scope=identify%20guilds'
  ].join('&')

  return `https://discord.com/api/oauth2/authorize?${params}`
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
    <Router>
      <div>
        <Link to="/" style={padding} >Home</Link>
        <Link to="/create" style={padding} >New Party</Link>
        <Link to="/parties" style={padding} >Parties</Link>
        { user
            ? <Link to={`/players/${user.id}`} >{user.name}</Link>
            : <a href={ getUrl() } >Login</a>
        }
      </div>

      <Switch>
        <Route path="/create">
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
  )
}

export default App
