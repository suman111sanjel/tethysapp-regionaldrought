<template>
  <el-row class="full-height">
    <el-col :span="4" class="full-height">
      <el-row class="first-row">
        <el-col :span="24" class="full-height full-width padding-left-10 padding-bottom-5 padding-top-10 padding-right-5">
          <mapControlsOutlook></mapControlsOutlook>
        </el-col>
      </el-row>
      <el-row class="second-row">
        <el-col :span="24"
                class="full-height full-width padding-left-10 padding-bottom-10 padding-top-5 padding-right-5">
          <usefulLinks></usefulLinks>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="16" class="full-height">
      <el-row class="first-row">
        <el-col :span="24" class="full-height full-width padding-left-5 padding-bottom-5 padding-top-10 padding-right-5">
          <mapComponentOutlook></mapComponentOutlook>
        </el-col>
      </el-row>
      <el-row class="second-row">
        <el-col :span="24" class="full-height full-width padding-left-5 padding-bottom-10 padding-top-5 padding-right-5">
          <chartComponent></chartComponent>
        </el-col>
      </el-row>
    </el-col>
    <el-col :span="4" class="full-height">
      <el-row class="first-row">
        <el-col :span="24"
                class="full-height full-width padding-left-5 padding-bottom-5 padding-top-10 padding-right-10">
          <LayerSwitcher></LayerSwitcher>
        </el-col>
      </el-row>
      <el-row class="second-row">
        <el-col :span="24"
                class="full-height full-width padding-left-5 padding-bottom-10 padding-top-5 padding-right-10">
          <about></about>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
import usefulLinks from "./usefulLinks";
import about from "./about";
import LayerSwitcher from "./LayerSwitcher";
import chartComponent from "./chartComponent";
import mapComponentOutlook from "./mapComponentOutlook";
import mapControlsOutlook from "./mapControlsOutlook";
export default {
  name: "outlookTabBody",
  components: {
    usefulLinks,
    about,
    LayerSwitcher,
    chartComponent,
    mapControlsOutlook,
    mapComponentOutlook,
  },
}
</script>

<style scoped>
.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.full-height {
  height: 100%;
}
</style>