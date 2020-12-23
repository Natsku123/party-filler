import {BaseApiService} from "./baseApiService";


class PlayerService extends BaseApiService {
    getCurrent = async () => {
        const response = await this.instance.get('');
        return response.data;
    }

    getIsSuperuser = async () => {
        const response = await this.instance.get('/superuser');
        return response.data;
    }
}

export const playerService = new PlayerService('/players');
