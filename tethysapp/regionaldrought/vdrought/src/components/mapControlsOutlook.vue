<template>
  <div class="card-box full-height full-width about-div">
    <div class="pannel-title">
      <h6 class="title-heading">Map Controls
      </h6>
    </div>
    <div class="body-container">
      <el-form ref="form" :model="form" label-width="100%" :inline="getIsInlineFormorNot" size="mini"
               label-position="left">
        <el-form-item label="Basin">
          <el-select v-model="form.basin" placeholder="Select Basin" class="full-width" @change="basinChange()">
            <el-option
                v-for="item in data.basin"
                :key="item.value"
                :label="item.label"
                :class="item.basin"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Select Indices">
          <el-select v-model="form.indices" placeholder="Select" @change="IndicesEnsembleChange()">
            <el-option
                v-for="item in data.indices"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Select Periodicity">
          <el-select v-model="form.periodicity" placeholder="Select">
            <el-option
                v-for="item in data.periodicityOutlook"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Filter Ensemble">
          <el-select v-model="form.ensemble" placeholder="Select" @change="IndicesEnsembleChange()">
            <el-option
                v-for="item in data.ensemble"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="submit-btn full-width">
          <el-button type="primary" class="full-width" @click="onSubmit">Process Outlook</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import {dataSelect} from '../utils/data'
import eventHub from "../utils/utils"
import {mapActions} from "vuex";
import {CollectHighchartRequiredInfo, CurrentDateFormat} from "../utils/helpers";

export default {
  name: "mapControlsOutlook",
  data() {
    return {
      form: {
        basin: '',
        indices: 'Tair_f_tavg',
        periodicity: 'monthly',
        ensemble: 'mean'
      },
      isInlineForm: true,
      data: dataSelect
    }
  }, methods: {
    ...mapActions(["ChartDataForecast"]),
    async onSubmit() {
      if (this.form.basin) {
        let date=CurrentDateFormat();
        let dataParam = {
          variable: this.form.indices,
          anominterval: this.form.periodicity,
          shapefile: 'true',
          distnum: this.form.basin,
          loc_type: 'Shapefile',
          ensemble: this.form.ensemble,
          date:date
        };
        const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        let data = await this.ChartDataForecast(dataParam);
        loading.close();
        let HChelpers = CollectHighchartRequiredInfo(this.form.periodicity, data['values'])
        let HighchartsObj =            {
          chart: {
            backgroundColor: 'rgba(255,255,255,0)',
            type: 'boxplot',
            animation: true,
            zoomType: 'x',
            // borderColor: '#000000',
            // borderWidth: 2,
          },
          title: {align: "center", text: 'Forecasted ' + data['anominterval'] + ' ' + data['name'] + ' Anomaly v Time'},
          xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
              month: '%e. %b',
              year: '%b'
            },
            title: {text: "Time (Months)"},
            tickInterval: HChelpers.tickInterval,
            tickPositioner: HChelpers.TickPositioner,
            labels: {
              formatter: HChelpers.Dateformater
            }
          },
          yAxis: {title: {text: 'Z Score'}},
          credits: {
            enabled: false
          },
          legend: {enabled: false},
          series: [{
            data: data['boxplot'],
            name: data['name'],
            tooltip: {valueSuffix: ' '},
          }],
        };


        console.log(HighchartsObj);
        eventHub.$emit('UpdateChart', HighchartsObj);
        console.log('submit!');
      } else {
        this.$message({
          message: 'Warning, Please select the basin.',
          type: 'warning'
        });
      }

    },
    getInLineData() {
      return this.isInlineForm
    },
    basinChange() {
      eventHub.$emit("basinChange", this.form.basin);
      this.$store.commit('setBasin', this.form.basin);
    },
    IndicesEnsembleChange() {
      eventHub.$emit("IndicesEnsembleChange", this.form.indices, this.form.ensemble);
      this.$store.commit('setIndices', this.form.indices);
      this.$store.commit('setEnsemble', this.form.ensemble);
    }
  },
  computed: {
    getIsInlineFormorNot() {
      return this.getInLineData();
    },
  },
  mounted() {
    this.$store.commit('setIndices', this.form.indices);
    this.$store.commit('setEnsemble', this.form.ensemble);
  },
}
</script>

<style scoped>

</style>