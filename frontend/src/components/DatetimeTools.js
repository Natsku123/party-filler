import moment from 'moment/moment';

export const toDate = (date) => moment.utc(date).toDate();