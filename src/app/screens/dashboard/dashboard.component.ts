import { Component, OnInit, AfterViewInit } from '@angular/core';
import { get } from 'scriptjs';
import { environment } from 'src/environments/environment';
import tempJSON from 'src/assets/home_nearby.json';
import { BackendService } from 'src/app/services/backend.service';
import { Place } from 'src/app/models/place';
import { MatSliderChange } from '@angular/material/slider';
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
  clickedLatLng: google.maps.LatLng = null;
  clickedCircle: google.maps.Circle = null;

  days: string[];
  colors: string[];
  // currentDate: Date;
  currentDay: number;
  currentHour: number;

  busyMeter: string[];
  places: Place[];

  constructor(private backend: BackendService) {
    this.days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    this.colors = ['#FFFFFF', '#FFD700', '#FFA500', '#FF0000'];
    const currentDate = new Date();
    this.currentDay = currentDate.getDay();
    this.currentHour = currentDate.getHours();

    this.busyMeter = ['Not crowded', 'A little crowded', 'Quite crowded', 'Very crowded'];
  }

  getDayFromIndex(index: number): string {
    const days: string[] = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return days[index];
  }

  getHourFromIndex(index: number): string {
    let h = index % 12;
    if (h === 0) { h = 12; }
    const partOfDay = Math.floor(index / 12) === 0 ? 'am' : 'pm';
    return h + partOfDay;
  }

  changeInDateTime(e: MatSliderChange) {
    console.log(e, this.currentDay, this.currentHour);
    this.updateMapData(null);
  }

  ngOnInit(): void {
  }

  ngAfterViewInit() {
    get('https://maps.googleapis.com/maps/api/js?key=' + environment.MAPS_API_KEY, () => {
      this.map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 34.052235, lng: -118.243683 },
        zoom: 17,
        clickableIcons: false
      });

      // Try HTML5 geolocation. Nah it only works on https
      let currentPos: google.maps.LatLng = new google.maps.LatLng(33.6704072, -117.8282598);
      const currentPosMarker = new google.maps.Marker({
        position: currentPos,
        map: this.map,
        icon: 'http://www.robotwoods.com/dev/misc/bluecircle.png',
      });
      this.map.setCenter(currentPos);

      // const input = document.getElementById('pac-input') as HTMLInputElement;
      // const searchBox = new google.maps.places.SearchBox(input);
      // this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

      // // Bias the SearchBox results towards current map's viewport.
      // this.map.addListener('bounds_changed', () => {
      //   searchBox.setBounds(this.map.getBounds());
      // });

      this.backend.getNearbyPopularTimes(currentPos.lat(), currentPos.lng()).subscribe((resp) => {
        console.log(resp);
        this.updateMapData(resp);
      });


      this.map.addListener('idle', () => {
        if (!currentPos.equals(this.map.getCenter())) {
          // same code repeated as above
          currentPos = this.map.getCenter();
          this.backend.getNearbyPopularTimes(currentPos.lat(), currentPos.lng()).subscribe((resp) => {
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
      circle.setMap(null);
    }
    this.circles.length = 0;

    if (resp != null) {
      this.places = Place.fromObjArr(resp);
      // if (this.clickedLocationWindow) {
      //   this.clickedLocationWindow.close();
      //   this.clickedLocationWindow = null;
      // }
    }

    const currentDayText = this.days[this.currentDay];
    for (const place of this.places) {

      let busynessIndex = Math.floor(place.popularTimes.find(p => p.day === currentDayText).times[this.currentHour] / 25);
      // For the extreme cases, pop >= 100
      if (busynessIndex > 3) { busynessIndex = 3; }
      const placeStatus: string = this.busyMeter[busynessIndex];
      const placeColor: string = this.colors[busynessIndex];
      // console.log(place.name, place.popularTimes.find(p => p.day === currentDayText).times[this.currentHour]);


      const circle = new google.maps.Circle({
        strokeColor: placeColor,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: placeColor,
        fillOpacity: 0.35,
        map: this.map,
        center: place.coordinates,
        radius: 10
      });

      google.maps.event.addListener(circle, 'click', (e) => {
        if (this.clickedLocationWindow) { this.clickedLocationWindow.close(); }
        this.clickedLocationWindow = new google.maps.InfoWindow();
        this.clickedLatLng = circle.getCenter();
        this.clickedCircle = circle;
        this.clickedLocationWindow.setContent(`<b>${place.name}</b><br>${placeStatus}`);
        this.clickedLocationWindow.setPosition(e.latLng);
        this.clickedLocationWindow.open(this.map);
        google.maps.event.addListener(this.clickedLocationWindow, 'closeclick', () => {
          this.clickedLocationWindow = null;
        });
      });
      this.circles.push(circle);
    }

    // const e = {
    //   latLng: new google.maps.LatLng(33.6676238, -117.8292908)
    // };
    // google.maps.event.trigger(this.circles[0], 'click', e);



    // Refresh the open window when sliders or center changes
    if (this.clickedLocationWindow) {
      this.clickedLocationWindow.close();
      for (const circle of this.circles) {
        if (circle.getCenter().equals(this.clickedLatLng)) {
          this.clickedCircle = circle;
          break;
        }
      }
      const e = {
        latLng: this.clickedLatLng
      };
      google.maps.event.trigger(this.clickedCircle, 'click', e);
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
