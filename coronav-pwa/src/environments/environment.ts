import credentials from './credentials.json';

// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

const SERVER_URL = 'http://192.168.0.101:5000/';

export const environment = {
  production: false,
  MAPS_API_KEY: credentials.MAPS_API_KEY,

  getNearbyPopularTimesURL: SERVER_URL + 'getNearbyPopularTimes6',
  getNearbyPlaceIdsURL: SERVER_URL + 'getNearbyPlaceIds',
  getSearchResultsURL: SERVER_URL + 'getSearchResults2',
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
