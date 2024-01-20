mapboxgl.accessToken =
  "pk.eyJ1IjoiY2xpbGxnZSIsImEiOiJjbHI1b3p1dDAwMDkzMmtscTUwaTg3YnhlIn0.uuDNJ1dtziwa-t9QYwyPxA";

const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/satellite-streets-v12",
  center: [-98, 38],
  zoom: 4.3,
});

let currentDataset = "2000-2004"; // Default dataset

async function loadGeoJsonData(dataset, perPage) {
  const response = await fetch(
    `/api/v1/geojson/${dataset}?page=1&per_page=${perPage}`
  );
  const data = await response.json();

  if (map.getSource("wildfires")) {
    map.getSource("wildfires").setData(data);
  } else {
    map.addSource("wildfires", {
      type: "geojson",
      data: data,
    });
    map.addLayer({
      id: "wildfires-heat",
      type: "heatmap",
      source: "wildfires",
      maxzoom: 9,
      paint: {
        "heatmap-weight": ["interpolate", ["linear"], ["zoom"], 0, 0, 9, 1],
        "heatmap-color": [
          "interpolate",
          ["linear"],
          ["heatmap-density"],
          0,
          "rgba(0, 0, 255, 0)",
          1,
          "rgba(255, 0, 0, 1)",
        ],
        "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 2, 9, 20],
        "heatmap-opacity": ["interpolate", ["linear"], ["zoom"], 7, 1, 9, 0],
      },
    });
  }
}

const layerList = document.getElementById("menu");
const inputs = layerList.getElementsByTagName("input");

map.on("load", () => {
  // Load initial data
  loadGeoJsonData(currentDataset, 500); // Load initial 500 features

  // Event listener for the scale slider
  const scaleSlider = document.getElementById("scale");
  scaleSlider.oninput = async () => {
    let numberOfFeatures = parseInt(scaleSlider.value);
    loadGeoJsonData(currentDataset, numberOfFeatures);
  };

  // Event listener for radio buttons
  for (const input of inputs) {
    if (input.type === "radio") {
      input.onclick = async (layer) => {
        currentDataset = layer.target.value;
        let numberOfFeatures = parseInt(scaleSlider.value);
        loadGeoJsonData(currentDataset, numberOfFeatures); // Load initial 500 features for new dataset
      };
    }
  }
});
