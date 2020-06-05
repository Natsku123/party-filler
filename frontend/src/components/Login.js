import React from 'react'

const handleDiscordLogin = () => {
  const params = [
    'client_id=SECRET',
    'scope=identify',
    'redirect_uri=coming_soon'
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
