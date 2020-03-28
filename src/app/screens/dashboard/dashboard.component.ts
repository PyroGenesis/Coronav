import { Component, OnInit, AfterViewInit } from '@angular/core';
import { get } from 'scriptjs';
import { environment } from 'src/environments/environment';
import tempJSON from 'src/assets/home_nearby.json';
// declare var google: any;
// Above not needed anymore as we edited tsconfig.app.json to include googlemaps types when compiling

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {

  map: google.maps.Map<HTMLElement>;

  constructor() { }

  ngOnInit(): void {
  }

  ngAfterViewInit() {
    get('https://maps.googleapis.com/maps/api/js?key=' + environment.MAPS_API_KEY, () => {
      this.map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 34.052235, lng: -118.243683 },
        zoom: 17
      });

      const wholesomeChoice = { lat: 33.664290, lng: -117.825285 };
      const infoWindow: google.maps.InfoWindow = new google.maps.InfoWindow();

      // Try HTML5 geolocation. Nah it only works on https
      // if (navigator.geolocation) {
      //   navigator.geolocation.getCurrentPosition((position) => {
      //     const pos = {
      //       lat: position.coords.latitude,
      //       lng: position.coords.longitude
      //     };

      //     infoWindow.setPosition(pos);
      //     infoWindow.setContent('Location found.');
      //     infoWindow.open(this.map);
      //     this.map.setCenter(pos);
      //   }, () => {
      //     this.handleLocationError(true, infoWindow, this.map.getCenter());
      //   });
      // } else {
      //   // Browser doesn't support Geolocation
      //   this.handleLocationError(false, infoWindow, this.map.getCenter());
      // }
      const currentPos = {
        lat: 33.6704072,
        lng: -117.8282598
      };
      const currentPosMarker = new google.maps.Marker({
        position: currentPos,
        map: this.map,
        icon: 'http://www.robotwoods.com/dev/misc/bluecircle.png',
      });
      this.map.setCenter(currentPos);

      const marker = new google.maps.Marker({
        position: wholesomeChoice,
        map: this.map,
      });

      const circles: google.maps.Circle[] = [];
      let clickedLocationWindow: google.maps.InfoWindow = null;

      for (const place of tempJSON.results) {
        // const box = place.geometry.viewport;
        // const verticalDelta = (box.northeast.lat - box.southwest.lat) / 4;
        // const horizontalDelta = (box.northeast.lng - box.southwest.lng) / 4;
        // console.log(verticalDelta, horizontalDelta);

        const circle = new google.maps.Circle({
          strokeColor: '#FF0000',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#FF0000',
          fillOpacity: 0.35,
          map: this.map,
          center: place.geometry.location,
          radius: 5
        });

        google.maps.event.addListener(circle, 'click', (e) => {
          if (clickedLocationWindow) { clickedLocationWindow.close(); }
          clickedLocationWindow = new google.maps.InfoWindow();
          clickedLocationWindow.setContent(place.name);
          clickedLocationWindow.setPosition(e.latLng);
          clickedLocationWindow.open(this.map);
        });

        circles.push(circle);

        // new google.maps.

        // rectangles.push(new google.maps.Rectangle({
        //   strokeColor: '#FF0000',
        //   strokeOpacity: 0.8,
        //   strokeWeight: 2,
        //   fillColor: '#FF0000',
        //   fillOpacity: 0.35,
        //   map: this.map,
        //   bounds: {
        //     north: box.northeast.lat - verticalDelta,
        //     south: box.southwest.lat + verticalDelta,
        //     east: box.northeast.lng - horizontalDelta,
        //     west: box.southwest.lng + horizontalDelta
        //   }
        // }));
        // break;
      }

      // const rectangle = new google.maps.Rectangle({
      //   strokeColor: '#FF0000',
      //   strokeOpacity: 0.8,
      //   strokeWeight: 2,
      //   fillColor: '#FF0000',
      //   fillOpacity: 0.35,
      //   map: this.map,
      //   bounds: {
      //     north: 33.6487673802915,
      //     south: 33.6460694197085,
      //     east: -117.8395834697085,
      //     west: -117.8422814302915
      //   }
      // });
    });

  }

  handleLocationError(browserHasGeolocation: boolean, infoWindow: any, pos: any) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
      'Error: The Geolocation service failed.' :
      'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(this.map);
  }
}

