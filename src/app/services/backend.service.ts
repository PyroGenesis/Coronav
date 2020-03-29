import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { switchMap, debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor(private http: HttpClient) { }

  getNearbyPopularTimes(lat: number, lng: number): Observable<any> {
    const params = new HttpParams()
      .append('lat', lat.toString())
      .append('lng', lng.toString());


    return this.http.get(environment.getNearbyPopularTimesURL, { params });
  }

  getSearchResults(searchTerm: string): Observable<any> {
    const params = new HttpParams()
      .append('text', searchTerm);

    return this.http.get(environment.getSearchResultsURL, { params });
  }
}
