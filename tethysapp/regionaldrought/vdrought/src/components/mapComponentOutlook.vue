<template>
  <div class="card-box full-height full-width about-div">
    <div id="map-container2">
    </div>
  </div>
</template>

<script>
import "ol/ol.css";
import Map from "ol/Map";
import OSM from "ol/source/OSM";
import TileLayer from "ol/layer/Tile";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import eventHub from "../utils/utils"
import {MajorBasinExtent, BasinExtent, mbasin, dataSelect, WMSSLD, legendImage} from "../utils/data";
import TimeDimensionTile from "ol-plus/layer/TimeDimensionTile";
import {ThreddsServer} from "../config";
import {CustomTimeDimensionalLayerDateLabel} from "../utils/helpers";

export default {
  name: "mapComponentOutlook",
  data() {
    return {
      mapObj: '',
      HighLightedLayer: '',
      view: '',
      mapObject: '',
      MajorBasin: '',
      AllLayers: '',
      initialLayerStartInterval: '',
      TimeSeriesLayerCollection: []
    }
  },
  methods: {
    mapInitilization() {
      let osm = new TileLayer({
        source: new OSM({attributions: [],}),
      });
      let TileLayers = new TileLayer({
        extent: [-13884991, 2870341, -7455066, 6338219],
        source: new TileWMS({
          url: "https://ahocevar.com/geoserver/wms",
          params: {LAYERS: "topp:states", TILED: true},
          serverType: "geoserver",
          // Countries have transparency, so do not fade tiles:
          transition: 0,
        }),
      });
      let view = new View({
        center: [9388155.512006583, 3291367.8109067543],
        zoom: 4
      });
      var map = new Map({
        layers: [],
        // target: this.$refs['map-root'],
        target: 'map-container2',
        view: view,
      });
      map.addLayer(osm);
      map.addLayer(TileLayers);

      var datasource = 'http://110.34.30.197:8080/geoserver/HKH/wms';
      var HighLightedLayer = new TileLayer({
        id: "highlightedlayer",
        title: "highlightedlayer",
        source: new TileWMS({
          url: datasource,
          hidpi: false,
          params: {
            'VERSION': '1.1.1',
          },
          serverType: 'geoserver'
        })
      });

      var MajorBasin = new TileLayer({
        id: "MajorBasin",
        title: "MajorBasin",
        visible: true,
        source: new TileWMS({
          url: datasource,
          hidpi: false,
          params: {
            'VERSION': '1.1.1',
            'LAYERS': 'HKH:MajorBasin',
            'STYLES': "MajorBasinStyle"
          },
          serverType: 'geoserver'
        }),
        zIndex: 50
      });

      HighLightedLayer.setZIndex(99);
      map.addLayer(HighLightedLayer);
      map.addLayer(MajorBasin);
      this.HighLightedLayer = HighLightedLayer;
      this.mapObject = map;
      this.view = view;
      this.MajorBasin = MajorBasin;
      this.addTimeDimensionLayer();
    },
    changeSelectedBasinOrMajorBasin(b) {
      console.log(b)
      let layerSource = this.HighLightedLayer.getSource();
      if (mbasin.includes(b)) {
        // basinChange();
        layerSource.updateParams({
          LAYERS: "HKH:MajorBasin",
          CQL_FILTER: "l1_name='" + b + "'",
          STYLES: "selected_Basin_SubBasin"
        });
        layerSource.tileCache.expireCache({});
        layerSource.tileCache.clear();
        layerSource.refresh();
        let myExtentString = MajorBasinExtent[b].replace(",", " ").split(" ");
        myExtentString.forEach(function (item, index) {
          myExtentString[index] = parseFloat(item);
        });
        this.view.fit(myExtentString, this.mapObject.getSize());

      } else {
        layerSource.updateParams({
          LAYERS: "HKH:Basin",
          CQL_FILTER: "l2_name='" + b + "'",
          STYLES: "selected_Basin_SubBasin"
        });
        layerSource.tileCache.expireCache({});
        layerSource.tileCache.clear();
        layerSource.refresh();
        let myExtentString = BasinExtent[b].replace(",", " ").split(" ");
        myExtentString.forEach(function (item, index) {
          myExtentString[index] = parseFloat(item);
        });
        this.view.fit(myExtentString, this.mapObject.getSize());
      }
    },
    layerSwitcher(tf) {
      this.MajorBasin.setVisible(tf);
    },
    changeSelectedIndicesEnsemble(indices, ensemble) {
      let mapObject = this.mapObject;
      for (let curLyrObj of this.TimeSeriesLayerCollection) {
        let newSelectedLayer = curLyrObj.getProperties().id === indices + '___' + ensemble;
        if (newSelectedLayer) {
          if (curLyrObj.getInitilizationStatus() === false) {
            curLyrObj.init().then((val) => {
                  mapObject.addThreddsLayer(val);
                  curLyrObj.setVisible(true);
                },
                (error) => {
                  console.error(error);
                });
          } else {
            curLyrObj.setVisible(true);
          }
        } else {
          if (curLyrObj.getInitilizationStatus() === true) {
            curLyrObj.setVisible(false);
          }
        }
      }
    },
    async addTimeDimensionLayer() {
      var mapObject = this.mapObject;
      var TimeSeriesLayerCollection = this.TimeSeriesLayerCollection;
      for (let curObj of dataSelect.indices) {
        for (let obj of dataSelect.ensemble) {
          let legendFetch = legendImage[curObj.value];
          let SLDD = WMSSLD[curObj.value];
          let legendImagePath = require('@/assets/legend/' + legendFetch);
          var mm = new TimeDimensionTile({
            id: curObj.value + '___' + obj.value,
            title: curObj.label,
            visible: false,
            opacity: 1,
            legendPath: legendImagePath,
            showlegend: true,
            ThreddsDataServerVersion: "5",
            dateisoFormatForLevelFormatter: CustomTimeDimensionalLayerDateLabel(this.$store.state.periodicity),
            timeSliderSize: "small",
            alignTimeSlider: "left",
            source: {
              url: ThreddsServer + '/wms/saldasforecast/monthly_std_' + obj.value + '.ncml',
              params: {
                'VERSION': "1.1.1",
                'LAYERS': curObj.value,
                'SLD_BODY': SLDD
              }
            }
          });
          TimeSeriesLayerCollection.push(mm);
        }
      }
      let aa = TimeSeriesLayerCollection.filter(function (x) {
        let prop = x.getProperties().id === 'Tair_f_tavg___mean';
        return prop
      })[0];
      if (aa.getInitilizationStatus() === false) {
        aa.init().then((val) => {
              mapObject.addThreddsLayer(val);
              aa.setVisible(true);
            },
            (error) => {
              console.error(error);
            });
      }
    }
  },
  created() {
  },
  mounted() {
    this.mapInitilization();
    eventHub.$on("basinChange", (b) => {
      this.changeSelectedBasinOrMajorBasin(b)
    });

    eventHub.$on("IndicesEnsembleChange", (indices, ensemble) => {
      this.changeSelectedIndicesEnsemble(indices, ensemble);
    });

    eventHub.$on("layerSwitcherSLDAS", (tf) => {
      let currentLay = this.$store.state.indices + '___' + this.$store.state.ensemble
      for (let curLyrObj of this.TimeSeriesLayerCollection) {
        let newSelectedLayer = curLyrObj.getProperties().id === currentLay;
        if (newSelectedLayer) {
          curLyrObj.setVisible(tf);
        }
      }
    });

    eventHub.$on("layerSwitcher", (tf) => {
      this.layerSwitcher(tf);
    });
  },
}
</script>

<style>
#map-container2 {
  height: 100%;
  width: 100%;
  border-radius: 5px;
}

#map-container2 .ol-viewport {
  border-radius: 5px;
}
</style>