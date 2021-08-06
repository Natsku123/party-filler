import { BaseApiService } from './baseApiService';


class PlayerService extends BaseApiService {
  getCurrent() {
    return this.instance.get('/').then(r => r.data);
  }

  getIsSuperuser() {
    return this.instance.get('/superuser').then(r => r.data);
  }

  getVisibleChannels() {
    return this.instance.get('/channels').then(r => r.data);
  }
}

export const playerService = new PlayerService('/players');
