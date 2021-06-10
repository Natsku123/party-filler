import { BaseApiService } from './baseApiService';


class PartyService extends BaseApiService {
  getMembers = (partyId) => {
    return this.instance.get(`/${partyId}/players`).then(r => r.data);

  create = (newObject, notify=false) => {
    return this.instance.post(`/?notify=${notify}`, newObject).then(r => r.data);
  };
}
const partyService = new PartyService('/parties');

export { partyService };
