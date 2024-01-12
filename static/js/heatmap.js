mapboxgl.accessToken = 'pk.eyJ1IjoiY2xpbGxnZSIsImEiOiJjbHI1b3p1dDAwMDkzMmtscTUwaTg3YnhlIn0.uuDNJ1dtziwa-t9QYwyPxA';

const url = 'https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson'

//const data = 

const layerList = document.getElementById('menu');
const inputs = layerList.getElementsByTagName('input');

var years = [];

var firstYears = [1992,1993,1994,1995,1996,1997,1998,1999];
var secondYears = [2000,2001,2002,2003,2004,2005,2006,2007];
var thirdYears = [2008,2009,2010,2011,2012,2013,2014,2015];

years.push(firstYears);
years.push(secondYears);
years.push(thirdYears);


//Need to remove current source/layer first THEN add the appropriate source/layer

//Could track the previous layer with a continuously updating variable 
//or remove any and all layers
for (const input of inputs) {
    input.onclick = (layer) => {
        const layerId = layer.target.id;
        const layerValue = layer.target.value;


        map.addSource('wildfires ' + layerId, {
            'type': 'geojson',
            'data': data.filter((result) => result.year in years[layerValue]),
        });
};
}


    const map = new mapboxgl.Map({
        container: 'map',
        // Choose from Mapbox's core styles
        style: 'mapbox://styles/mapbox/satellite-streets-v12',
        center: [-98, 38],
        zoom: 4.3
    });
 
    map.on('load', () => {
    // Add a geojson point source.
    // Heatmap layers also work with a vector tile source.
        map.addSource('earthquakes', {
            'type': 'geojson',
            'data': 'https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson'
        });
        // This map source is temporary. Should be replaced with the input.onclick code above 
        // eventually to change the data depending on which timeframe is selected.

        map.addLayer(
        {
        'id': 'earthquakes-heat',
        'type': 'heatmap',
        'source': 'earthquakes',
        'maxzoom': 9,
        'paint': {
            // Increase the heatmap weight based on frequency and property magnitude
                'heatmap-weight': [
                    'interpolate',
                    ['linear'],
                    ['get', 'mag'],
                    0,
                    0,
                    6,
                    1
                ],
                // Increase the heatmap color weight weight by zoom level
                // heatmap-intensity is a multiplier on top of heatmap-weight
                'heatmap-intensity': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    0,
                    1,
                    9,
                    3
                ],
                // Color ramp for heatmap.  Domain is 0 (low) to 1 (high).
                // Begin color ramp at 0-stop with a 0-transparancy color
                // to create a blur-like effect.
                'heatmap-color': [
                    'interpolate',
                    ['linear'],
                    ['heatmap-density'],
                    0,
                    'rgba(222, 175, 22, 0)',
                    0.2,
                    'rgb(222, 150, 22)',
                    0.4,
                    'rgb(222, 125, 22)',
                    0.6,
                    'rgb(222, 100, 22)',
                    0.8,
                    'rgb(222, 50, 22)',
                    1,
                    'rgb(222, 25, 22)'
                ],
                // Adjust the heatmap radius by zoom level
                'heatmap-radius': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    0,
                    2,
                    9,
                    20
                ],
                // Transition from heatmap to circle layer by zoom level
                'heatmap-opacity': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    7,
                    1,
                    9,
                    0
                ]
            }
        },
        'waterway-label'
    );

    // Possible Junk Code for our purposes
    map.addLayer(
        {
            'id': 'earthquakes-point',
            'type': 'circle',
            'source': 'earthquakes',
            'minzoom': 7,
            'paint': {
                // Size circle radius by earthquake magnitude and zoom level
                'circle-radius': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    7,
                    ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4],
                    16,
                    ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 50]
                ],
                // Color circle by earthquake magnitude
                'circle-color': [
                    'interpolate',
                    ['linear'],
                    ['get', 'mag'],
                    1,
                    'rgba(33,102,172,0)',
                    2,
                    'rgb(103,169,207)',
                    3,
                    'rgb(209,229,240)',
                    4,
                    'rgb(253,219,199)',
                    5,
                    'rgb(239,138,98)',
                    6,
                    'rgb(178,24,43)'
                ],
                'circle-stroke-color': 'white',
                'circle-stroke-width': 1,
                // Transition from heatmap to circle layer by zoom level
                'circle-opacity': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    7,
                    0,
                    8,
                    1
                ]
            }
        },
        'waterway-label'
    );
});