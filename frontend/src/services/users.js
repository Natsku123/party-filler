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
