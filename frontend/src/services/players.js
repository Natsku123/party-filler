import axios from 'axios'

const baseUrl = 'http://api.party.hellshade.fi/players'

const instance = axios.create({
    baseURL: baseUrl,
    withCredentials: true
})

instance.interceptors.request.use(
  (config) => {
    config.headers.withCredentials = true
    return config
  }, (err) => Promise.reject(err)
)

const getUser = async () => {
  const response = await instance.get('')
  return response.data
}

const getUserById = async (id) => {
  const response = await instance.get(`/${id}`)
  return response.data
}

export default {
  getUser,
  getUserById,
}
