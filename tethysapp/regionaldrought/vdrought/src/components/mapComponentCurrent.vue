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
import eventHub from "../utils/utils";
import {MajorBasinExtent, BasinExtent, mbasin, WMSSLDCurrent, dataSelect} from "../utils/data";
import {mapActions} from "vuex";
import TimeDimensionTile from "ol-plus/layer/TimeDimensionTile";
import {CustomTimeDimensionalLayerDateLabel} from '../utils/helpers';

// import {MajorBasinExtent, BasinExtent, mbasin, dataSelect, WMSSLD, legendImage} from "../utils/data";
// import TimeDimensionTile from "ol-plus/layer/TimeDimensionTile";
// import {ThreddsServer} from "../utils/config";

export default {
  name: "mapComponentCurrent",
  data() {
    return {
      mapObj: '',
      HighLightedLayer: '',
      view: '',
      mapObject: '',
      MajorBasin: '',
      AllLayers: '',
      TimeSeriesLayerCollection: [],
      selectedFilesOnAYear: []
    }
  },
  methods: {
    ...mapActions(["SlicingThreddsCatalog"]),
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
    changeIndicesPeriodicityYear() {

    },
    async loadTimeSeriesData(indices, periodicity, year) {
      let WMSAndPeriodKey = periodicity + '___' + year.toString();
      var selectedFioYear = this.selectedFilesOnAYear.filter(function (x) {
        let keyList = Object.keys(x);
        return keyList.includes(WMSAndPeriodKey);
      });
      let obj1 = {};
      if (!selectedFioYear.length) {
        let data = await this.SlicingThreddsCatalog({periodicity, year});
        obj1[WMSAndPeriodKey] = data;
        this.selectedFilesOnAYear.push(obj1);
        return data;
      } else {
        return selectedFioYear[0][WMSAndPeriodKey];
      }
    },
    async addTimeDimensionLayer() {
      var mapObject = this.mapObject;
      var layerId = this.$store.state.indices + '___' + this.$store.state.periodicity + '___' + this.$store.state.year;
      var selectedLayr = this.TimeSeriesLayerCollection.filter(function (x) {
        var checkLayer = x.getProperties().id === layerId;
        if (!checkLayer) {
          x.setVisible(false);
          console.log("fdkfkasdfk")
        }
        console.log("----------------------------------");
        console.log(x);
        return checkLayer;
      });
      if (selectedLayr.length) {
        if (selectedLayr.length === 1) {
          selectedLayr[0].setVisible(true);
        } else {
          console.log("there are multiple layer added!!!!");
        }
      } else {
        let WMSList = await this.loadTimeSeriesData(this.$store.state.indices, this.$store.state.periodicity, this.$store.state.year);
        console.log(WMSList);
        let curObj = dataSelect.indices.filter(x => x.value == this.$store.state.indices)[0];
        let SLDD = WMSSLDCurrent[curObj.value];
        let legendUrl = WMSList[0] + `?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetLegendGraphic&WIDTH=10&HEIGHT=230&LAYERS=${curObj.value}&SLD_BODY=${encodeURIComponent(SLDD).toString()}`;

        var mm = new TimeDimensionTile({
          id: layerId,
          title: curObj.label,
          visible: true,
          opacity: 1,
          legendPath: legendUrl,
          showlegend: true,
          ThreddsDataServerVersion: "5",
          dateisoFormatForLevelFormatter:CustomTimeDimensionalLayerDateLabel(this.$store.state.periodicity),
          timeSliderSize: "small",
          alignTimeSlider: "left",
          source: {
            url: WMSList,
            params: {
              'VERSION': "1.1.1",
              'LAYERS': curObj.value,
              'SLD_BODY': SLDD
            }
          }
        });
        await mm.init().then((val) => {
              mapObject.addThreddsLayer(val);
              mm.setVisible(true);
            },
            (error) => {
              console.error(error);
            });
        this.TimeSeriesLayerCollection.push(mm);
      }
    }
  },
  created() {
  },

  mounted() {
    this.mapInitilization();
    eventHub.$on("basinChange", (b) => {
      this.changeSelectedBasinOrMajorBasin(b);
    });
    eventHub.$on("indicesPeriodicityYearChange", () => {
      this.addTimeDimensionLayer();
    });
    eventHub.$on("layerSwitcherSLDAS", (tf) => {
      var currentLay = this.$store.state.indices + '___' + this.$store.state.periodicity + '___' + this.$store.state.year;
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