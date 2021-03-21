import { BaseApiService } from './baseApiService';


class MemberService extends BaseApiService {
    create = async (newObject, notify= false) => {
        const response = await this.instance.post(`/?notify=${notify}`, newObject);
        return response.data;
    };
}

export const memberService = new MemberService('/members');

