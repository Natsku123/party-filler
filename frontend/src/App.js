import React from 'react'
import {
  BrowserRouter as Router,
  Switch, Route, Link
} from "react-router-dom"

import Login from './components/Login'
import PartyForm from './components/PartyForm'
import Parties from './components/Parties'

const App = () => {
  const padding = {
    padding: 5
  }

  return (
    <Router>
      <div>
        <Link to="/" style={padding} >Home</Link>
        <Link to="/login" style={padding} >Login</Link>
        <Link to="/create" style={padding} >New Party</Link>
        <Link to="/parties" style={padding} >Parties</Link>
      </div>

      <Switch>
        <Route path="/login">
          <Login/>
        </Route>
        <Route path="/create">
          <PartyForm />
        </Route>
        <Route path="/parties">
          <Parties />
        </Route>
        <Route path="/">
          <h1>Home Page</h1>
        </Route>
      </Switch>

    </Router>
  )
}

export default App
