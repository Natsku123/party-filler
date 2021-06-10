import axios from 'axios';

const baseUrl = ((window.REACT_APP_API_HOSTNAME) ? window.REACT_APP_API_HOSTNAME : 'http://localhost:8800');

class BaseApiService {

  constructor(prefix='') {
    this.instance = axios.create({
      baseURL: baseUrl + prefix,
      withCredentials: true
    });

    this.instance.interceptors.request.use(
      (config) => {
        config.headers.withCredentials = true;
        return config;
      }, (err) => Promise.reject(err)
    );
  }

  getAll = (skip=0, limit=100) => {
    return this.instance.get(`/?skip=${skip}&limit=${limit}`).then(r => r.data);
  };

  getOne = (id) => {
    return this.instance.get(`/${id}`).then(r => r.data);
  };

  create = (newObject) => {
    return this.instance.post('/', newObject).then(r => r.data);
  };

  update = (id, newObject) => {
    return this.instance.put(`/${id}`, newObject).then(r => r.data);
  };

  remove = (id) => {
    return this.instance.delete(`/${id}`).then(r => r.data);
  };
}

export { BaseApiService };
