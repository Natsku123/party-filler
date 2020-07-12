import axios from 'axios'

const baseUrl = 'http://api.party.hellshade.fi/channels'

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

const create = async (channelObj) => {
  const response = await instance.post('', channelObj)
  return response.data
}

export default {
  create,
}
