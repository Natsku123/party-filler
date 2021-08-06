import { BaseApiService } from './baseApiService';


class MemberService extends BaseApiService {
  create(newObject, notify=false) {
    return this.instance.post(`/?notify=${notify}`, newObject).then(r => r.data);
  }
}

export const memberService = new MemberService('/members');

