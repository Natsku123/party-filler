import { BaseApiService } from './baseApiService';


class PartyService extends BaseApiService {
  getMembers = async (partyId) => {
    const response = await this.instance.get(`/${partyId}/players`);
    return response.data;
  };
  create = async (newObject, notify=false) => {
    return new Promise((resolve, reject) => {
      this.instance.post(`/?notify=${notify}`, newObject).then(r => resolve(r.data)).catch(reject);
    });
  };
}
const partyService = new PartyService('/parties');

export { partyService };
