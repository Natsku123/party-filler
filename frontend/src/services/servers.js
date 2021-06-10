import {BaseApiService} from "./baseApiService";


class ServerService extends BaseApiService {
  getChannels = (id) => {
    return this.instance.get(`/${id}/channels`).then(r => r.data);
  };
}

export const serverService = new ServerService('/servers');
