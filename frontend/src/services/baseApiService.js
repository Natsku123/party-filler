import axios from 'axios';

const baseUrl = ((window.REACT_APP_API_HOSTNAME) ? window.REACT_APP_API_HOSTNAME : 'http://localhost:8800');

class BaseApiService {

    constructor(prefix = "") {
        this.instance = axios.create({
            baseURL: baseUrl + prefix,
            withCredentials: true
        });

        this.instance.interceptors.request.use(
            (config) => {
                config.headers.withCredentials = true
                return config
            }, (err) => Promise.reject(err)
        );
    }

    getAll = async (skip = 0, limit = 100) => {
        return new Promise(async (resolve, reject) => {
            this.instance.get(`/?skip=${skip}&limit=${limit}`).then(r => resolve(r.data)).catch(reject);
        });
    };

    getOne = async (id) => {
        return new Promise(async (resolve, reject) => {
            this.instance.get(`/${id}`).then(r => resolve(r.data)).catch(reject);
        });
    };

    create = async (newObject) => {
        return new Promise(async (resolve, reject) => {
            this.instance.post('/', newObject).then(r => resolve(r.data)).catch(reject);
        });
    };

    update = async (id, newObject) => {
        return new Promise(async (resolve, reject) => {
            this.instance.put(`/${id}`, newObject).then(r => resolve(r.data)).catch(reject);
        });
    };

    remove = async(id) => {
        return new Promise(async (resolve, reject) => {
            this.instance.delete(`/${id}`).then(r => resolve(r.data)).catch(reject);
        });
    };
}

export { BaseApiService };