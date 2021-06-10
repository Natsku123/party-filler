import { BaseApiService } from './baseApiService';


class PartyService extends BaseApiService {
  getMembers = (partyId) => {
    return this.instance.get(`/${partyId}/players`).then(r => r.data);
  };
}
const partyService = new PartyService('/parties');

export { partyService };
