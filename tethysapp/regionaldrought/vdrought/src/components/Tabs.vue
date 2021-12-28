<template>
  <el-tabs type="border-card" class="tabs-outer" height="28px" v-model="currentTab" @tab-click="changePage">
    <el-tab-pane key="current" name="current" label="Current" class="full-height" >
      <currentTabBody v-if="currentTab ==='current'"></currentTabBody>
    </el-tab-pane>
    <el-tab-pane key="outlook" name="outlook" label="Outlook" class="full-height">
      <outlookTabBody  v-if="currentTab !='current'"></outlookTabBody>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import {TethysAppName} from "../config";
import currentTabBody from "./currentTabBody";
import outlookTabBody from "./outlookTabBody";

export default {
  name: "Tabs",
  props: {
    activeTab: {
      type: String,
      required: true
    },
  },
  components: {
    currentTabBody,
    outlookTabBody,
  },
  data() {
    return {selectedTab: 'current'}
  },
  methods: {
    changePage(evt) {
      var download = document.createElement('a');
      // if (process.env.NODE_ENV === "development") {
      //   if (evt.props.name === "current") {
      //     download.href = "/current/";
      //   } else {
      //     download.href = "/outlook/";
      //   }
      // } else {
        if (evt.props.name === "current") {
          download.href = "/apps/" + TethysAppName + "/current/";
        } else {
          download.href = "/apps/" + TethysAppName + "/outlook/";
        }
      // }
      download.click();
    },
    getCurrentTab() {
      return this.activeTab
    }
  },
  computed: {
    currentTab() {
      return this.getCurrentTab()
    },
  }
}
</script>

<style lang="scss">
.tabs-outer {
  width: 100%;
}


.tabs-outer .el-tabs__nav-scroll, .tabs-outer .el-tabs__nav.is-top, .el-tabs__item {
  height: 28px;
}

.el-tabs__item.is-active {
  height: 29px;
}

.el-tabs__nav-scroll {
  background-color: rgb(60, 126, 165);
  color: white;
}

.el-tabs--border-card {
  border: 0px solid #DCDFE6;
}

.tabs-outer .el-tabs__item {
  color: white !important;
}

.el-tabs__item.is-active {
  background-color: #9cb4be !important;
  border-right-color: #9cb4be !important;
  border-left-color: #9cb4be !important;
}

.el-tabs__content {
  background-color: #9cb4be !important;
}

.el-tabs__item {
  line-height: 32px
}

.el-tabs__content {
  height: calc(100% - 28px);
  padding: 0px !important;
}
.full-height{
  height: 100%;
}
</style>