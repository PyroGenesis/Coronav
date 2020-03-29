export class Place {
    name: string;
    address: string;
    id: string;
    coordinates: google.maps.LatLng;
    popularTimes: {
        day: string;
        times: number[]
    }[];

    constructor(placeObj: any) {
        this.name = placeObj.details.name;
        this.address = placeObj.details.address;
        this.id = placeObj.details.id;
        this.coordinates = new google.maps.LatLng (
            placeObj.details.coordinates.lat,
            placeObj.details.coordinates.lng,
        );
        this.popularTimes = [];
        for (const pt of placeObj.details.populartimes) {
            this.popularTimes.push({
                day: pt.name,
                times: pt.data
            });
        }
    }

    static fromObjArr(placeObjArr: any): Place[] {
        const res: Place[] = [];
        for (const p of placeObjArr.places) {
            res.push(new Place(p));
        }
        return res;
    }
}

export class SearchPlace {
    name: string;
    address: string;
    id: string;
    coordinates: google.maps.LatLng;
    viewport: {
        northeast: google.maps.LatLng;
        southwest: google.maps.LatLng;
    };
    hasPopularTimes: boolean;
    popularTimes: {
        day: string;
        times: number[]
    }[];

    constructor(placeObj: any) {
        this.name = placeObj.details.name;
        this.address = placeObj.details.address;
        this.id = placeObj.details.id;
        this.coordinates = new google.maps.LatLng (
            placeObj.geometry.location.lat,
            placeObj.geometry.location.lng,
        );
        this.viewport = {
            northeast: new google.maps.LatLng (
                placeObj.geometry.viewport.northeast.lat,
                placeObj.geometry.viewport.northeast.lng,
            ),
            southwest: new google.maps.LatLng (
                placeObj.geometry.viewport.southwest.lat,
                placeObj.geometry.viewport.southwest.lng,
            )
        };
        this.popularTimes = [];
        this.hasPopularTimes = placeObj.hasPopularTimes;
        if (placeObj.hasPopularTimes) {
            for (const pt of placeObj.details.populartimes) {
                this.popularTimes.push({
                    day: pt.name,
                    times: pt.data
                });
            }
        }
    }
}
