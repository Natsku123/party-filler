import { memberService } from './members';

export const joinParty = async (partyId, playerId, roleId = null, playerReq = null, notify = false) => {
  return await memberService.create({
    partyId,
    playerId,
    roleId,
    playerReq
  }, notify);
};

export const leaveParty = async (memberId) => {
  return await memberService.remove(memberId);
};