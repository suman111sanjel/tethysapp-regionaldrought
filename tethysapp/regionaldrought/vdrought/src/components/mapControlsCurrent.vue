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
          <el-select v-model="form.indices" placeholder="Select" @change="indicesPeriodicityYearChange()">
            <el-option
                v-for="item in data.indices"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Select Periodicity">
          <el-select v-model="form.periodicity" placeholder="Select" @change="indicesPeriodicityYearChange()">
            <el-option
                v-for="item in data.periodicity"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Select Year">
          <el-select v-model="form.year" placeholder="Select" @change="indicesPeriodicityYearChange()">
            <el-option
                v-for="item in data.year"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="submit-btn full-width">
          <el-button type="primary" class="full-width" @click="onSubmit">Get Current Average</el-button>
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
  name: "mapControlsCurrent",
  data() {
    return {
      form: {
        basin: '',
        indices: '',
        periodicity: '',
        year: ''
      },
      isInlineForm: true,
      data: dataSelect
    }
  }, methods: {
    ...mapActions(["ChartDataCurrent"]),
    async onSubmit() {
      if (this.form.basin) {
        let date=CurrentDateFormat();
        let dataParam = {
          variable: this.form.indices,
          anominterval: this.form.periodicity,
          year: this.form.year.toString(),
          shapefile: 'true',
          distnum: this.form.basin,
          datatype: 'Current',
          date:date
        };
        const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        let data = await this.ChartDataCurrent(dataParam);
        loading.close();
        let HChelpers = CollectHighchartRequiredInfo(this.form.periodicity, data['values'])
        let HighchartsObj = {
          chart: {
            backgroundColor: 'rgba(255,255,255,0)',
            type: 'area',
            animation: true,
            zoomType: 'x',
            // borderColor: '#000000',
            // borderWidth: 2,
          },
          title: {align: "center", text: data['anominterval'] + ' ' + data['name'] + ' v Time'},
          xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
              month: '%e. %b',
              year: '%b'
            },
            title: {text: "Time"},
            tickInterval: HChelpers.tickInterval,
            tickPositioner: HChelpers.TickPositioner,
            labels: {
              formatter: HChelpers.Dateformater
            }
          },
          yAxis: {title: {text: data['units']}},
          tooltip: {
            useHTML: true,
            shared: true,
            formatter: HChelpers.TootTipFormatter
          },
          credits: {
            enabled: false
          },
          series: [{
            data: data['values'],
            type: "spline",
            name: data['name'],
            tooltip: { valueSuffix: ' '+data['units']},
          }],
        };
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
      this.$store.commit('setBasin', this.form.basin);
      eventHub.$emit("basinChange", this.form.basin);
    },
    indicesPeriodicityYearChange() {
      this.$store.commit('setIndices', this.form.indices);
      this.$store.commit('setPeriodicity', this.form.periodicity);
      this.$store.commit('setYear', this.form.year);
      eventHub.$emit("indicesPeriodicityYearChange");
    }
  },
  computed: {
    getIsInlineFormorNot() {
      return this.getInLineData()
    },
  },
  created() {
    this.form.basin = this.$store.state.basin;
    this.form.indices = this.$store.state.indices;
    this.form.periodicity = this.$store.state.periodicity;
    this.form.year = this.$store.state.year;
  },
}
</script>

<style scoped>

</style>