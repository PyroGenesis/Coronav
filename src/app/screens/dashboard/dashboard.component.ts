import { Component, OnInit, AfterViewInit } from '@angular/core';
import { get } from 'scriptjs';
import { environment } from 'src/environments/environment';
import tempJSON from 'src/assets/home_nearby.json';
import { BackendService } from 'src/app/services/backend.service';
import { Place } from 'src/app/models/place';
// declare var google: any;
// Above not needed anymore as we edited tsconfig.app.json to include googlemaps types when compiling

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {

  map: google.maps.Map<HTMLElement>;
  circles: google.maps.Circle[] = [];
  clickedLocationWindow: google.maps.InfoWindow = null;

  days: string[];
  currentDay: string;
  currentHour: number;

  busyMeter: string[];
  places: Place[];

  constructor(private backend: BackendService) {
    this.days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const currentDate = new Date();
    this.currentDay = this.days[currentDate.getDay()];
    this.currentHour = currentDate.getHours();

    this.busyMeter = ['Not crowded', 'A little crowded', 'Quite crowded', 'Very crowded'];
  }

  ngOnInit(): void {
  }

  ngAfterViewInit() {
    get('https://maps.googleapis.com/maps/api/js?key=' + environment.MAPS_API_KEY, () => {
      this.map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 34.052235, lng: -118.243683 },
        zoom: 17
      });

      // Try HTML5 geolocation. Nah it only works on https
      const currentPos: google.maps.LatLng = new google.maps.LatLng(33.6704072, -117.8282598);
      const currentPosMarker = new google.maps.Marker({
        position: currentPos,
        map: this.map,
        icon: 'http://www.robotwoods.com/dev/misc/bluecircle.png',
      });
      this.map.setCenter(currentPos);

      this.backend.getNearbyPopularTimes(33.6471628, -117.8411294).subscribe((resp) => {
        console.log(resp);
        this.updateMapData(resp);
      });


      this.map.addListener('idle', () => {
        if (!currentPos.equals(this.map.getCenter())) {
          // same code repeated as above
          this.backend.getNearbyPopularTimes(33.6471628, -117.8411294).subscribe((resp) => {
            console.log(resp);
            this.updateMapData(resp);
          });
        }
      });

    });
  }

  updateMapData(resp: any) {

    for (const circle of this.circles) {
      google.maps.event.clearListeners(circle, 'click');
    }
    this.circles.length = 0;
    if (this.clickedLocationWindow) { this.clickedLocationWindow.close(); }

    this.places = Place.fromObjArr(resp);
    for (const place of this.places) {

      const placeStatus = this.busyMeter[Math.floor(place.popularTimes.find(p => p.day === this.currentDay).times[this.currentHour] / 25)];
      // console.log(place.popularTimes.find(p => p.day === this.currentDay).times[this.currentHour]);


      const circle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: this.map,
        center: place.coordinates,
        radius: 5
      });

      google.maps.event.addListener(circle, 'click', (e) => {
        if (this.clickedLocationWindow) { this.clickedLocationWindow.close(); }
        this.clickedLocationWindow = new google.maps.InfoWindow();
        this.clickedLocationWindow.setContent(`<b>${place.name}<\b><br>${placeStatus}`);
        this.clickedLocationWindow.setPosition(e.latLng);
        this.clickedLocationWindow.open(this.map);
      });

      this.circles.push(circle);
    }
  }

  handleLocationError(browserHasGeolocation: boolean, infoWindow: any, pos: any) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
      'Error: The Geolocation service failed.' :
      'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(this.map);
  }
}
