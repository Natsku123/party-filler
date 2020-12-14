import axios from 'axios'

const baseUrl = ((window.REACT_APP_API_HOSTNAME) ? window.REACT_APP_API_HOSTNAME : 'http://localhost:8800');

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
