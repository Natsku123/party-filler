import React from 'react'

const handleDiscordLogin = () => {
  const params = [
    'client_id=718047907617439804',
    'redirect_uir=http%3A%2F%2Fapi.party.hellshade.fi%2Foauth2%2Fcallback',
    'response_type=code',
    'scope=identify%20guilds'
  ].join('&')

  window.location.assign(`https://discord.com/api/oauth2/authorize?${params}`)
}

const Login = () => {
  return (
    <div>
      <h2>Login</h2>
      <button onClick={handleDiscordLogin} >Discord</button>
    </div>
  )
}

export default Login
