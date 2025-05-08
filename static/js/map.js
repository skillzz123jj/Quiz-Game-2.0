'use strict';

//Gets the map from OpenFreeMap
export const map = new maplibregl.Map({
  container: 'map',
  style: 'https://tiles.openfreemap.org/styles/liberty',
  center: [13.388, 52.517],
  zoom: 2.5,
});

//Disables some built-in features in the map
map.dragPan.disable();
map.dragRotate.disable();
map.scrollZoom.disable();
map.doubleClickZoom.disable();
map.touchZoomRotate.disable();
map.on('load', () => {
  loadCountryGeoJSON(map);
});

//Finds the location of each country and and adds a dot over it on the map
export async function loadCountryGeoJSON(map) {
  const completedRes = await fetch('/get-countries');
  const completedData = await completedRes.json();
  const completedCountries = completedData.countries || [];

  const res = await fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json');
  const geojson = await res.json();

  geojson.features.forEach((feature) => {
    const name = feature.properties.name;
    const [minLon, minLat, maxLon, maxLat] = getBounds(feature.geometry.coordinates);
    const lat = (minLat + maxLat) / 2;
    const lon = (minLon + maxLon) / 2;

    if (!isNaN(lat) && !isNaN(lon)) {
      const el = document.createElement('div');
        el.className = 'country-dot';
        el.title = name;

        if (completedCountries.includes(name)) {
        el.style.backgroundColor = 'green';
        el.classList.add('collected');
      }

      new maplibregl.Marker({element: el})
        .setLngLat([lon, lat])
        .addTo(map);
    }
  });
}

function getBounds(coords) {
  let lons = [], lats = [];

  function extract(coordSet) {
    for (const coord of coordSet) {
      if (typeof coord[0][0] === 'number') {
        for (const [lon, lat] of coord) {
          lons.push(lon);
          lats.push(lat);
        }
      } else {
        extract(coord);
      }
    }
  }

  extract(coords);
  return [Math.min(...lons), Math.min(...lats), Math.max(...lons), Math.max(...lats)];
}
