import { BaseApiService } from './baseApiService';


class PartyService extends BaseApiService {
    getMembers = async (partyId) => {
        const response = await this.instance.get(`/${partyId}/players`)
        return response.data
    };
}
const partyService = new PartyService('/parties');

export { partyService };