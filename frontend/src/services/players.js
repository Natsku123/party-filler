import {BaseApiService} from "./baseApiService";


class PlayerService extends BaseApiService {
  getCurrent = () => {
    return new Promise((resolve, reject) => {
      this.instance.get('').then(r => resolve(r.data)).catch(reject);
    });
  };

  getIsSuperuser = () => {
    return new Promise((resolve, reject) => {
      this.instance.get('/superuser').then(r => resolve(r.data)).catch(reject);
    });
  };

  getVisibleChannels = () => {
    return new Promise((resolve, reject) => {
      this.instance.get('/channels').then(r => resolve(r.data)).catch(reject);
    });
  };
}

export const playerService = new PlayerService('/players');
