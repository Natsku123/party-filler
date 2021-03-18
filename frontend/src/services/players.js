import {BaseApiService} from "./baseApiService";


class PlayerService extends BaseApiService {
    getCurrent = async () => {
        return new Promise(async (resolve, reject) => {
            this.instance.get('').then(r => resolve(r.data)).catch(reject);
        });
    };

    getIsSuperuser = async () => {
        return new Promise(async (resolve, reject) => {
            this.instance.get('/superuser').then(r => resolve(r.data)).catch(reject);
        });
    };

    getVisibleChannels = async () => {
        return new Promise(async (resolve, reject) => {
            this.instance.get('/channels').then(r => resolve(r.data)).catch(reject);
        });
    };
}

export const playerService = new PlayerService('/players');
