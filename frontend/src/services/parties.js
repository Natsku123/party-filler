import axios from 'axios'

const baseUrl = 'http://api.party.hellshade.fi/parties'

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

const getAll = async () => {
  const response = await instance.get('')
  return response.data
}

const getPage = async (page, per) => {
  const response = await instance.get(`/page/${page}/per/${per}`)
  return response.data
}

const getOne = async (partyId) => {
  const response = await instance.get(`/${partyId}`)
  return response.data
}

const create = async (newParty) => {
  const response = instance.post('', newParty)
  return response.data
}

const update = async (partyId, newParty) => {
  const response = await instance.put(`/${partyId}`, newParty)
  return response.data
}

const remove = async (partyId) => {
  const response = await instance.delete(`/${partyId}`)
  return response.data
}

const join = async (partyId, playerId) => {
  const response = await instance.post(`${partyId}/players`, playerId)
  return response.data
}

const leave = async (partyId, playerId) => {
  const response = await instance.delete(`${partyId}/players/${playerId}`)
  return response.data
}

export default {
  getAll,
  getPage,
  getOne,
  create,
  update,
  remove,
  join,
  leave
}
