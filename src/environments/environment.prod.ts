import credentials from './credentials.json';

const SERVER_URL = 'http://192.168.0.101:5000/';

export const environment = {
  production: true,
  MAPS_API_KEY: credentials.MAPS_API_KEY,

  getNearbyPopularTimesURL: SERVER_URL + 'getNearbyPopularTimes6',
  getNearbyPlaceIdsURL: SERVER_URL + 'getNearbyPlaceIds',
  getSearchResultsURL: SERVER_URL + 'getSearchResults2',
};
