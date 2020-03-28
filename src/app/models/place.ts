export class Place {
    id: string;
    coordinates: google.maps.LatLng;
    name: string;
    popularTimes: {
        day: string;
        times: number[]
    }[];

    constructor(placeObj: any) {
        this.id = placeObj.details.id;
        this.coordinates = new google.maps.LatLng (
            placeObj.details.coordinates.lat,
            placeObj.details.coordinates.lng,
        );
        this.name = placeObj.details.name;
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

// export class PopularTime {

// }
