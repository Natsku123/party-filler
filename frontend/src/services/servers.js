import {BaseApiService} from "./baseApiService";


class ServerService extends BaseApiService {
  getChannels = async (id) => {
    const response = await this.instance.get(`/${id}/channels`);
    return response.data;
  };
}

export const serverService = new ServerService('/servers');
