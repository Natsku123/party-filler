import {BaseApiService} from "./baseApiService";


class GameService extends BaseApiService {
}

export const gameService = new GameService('/games');
