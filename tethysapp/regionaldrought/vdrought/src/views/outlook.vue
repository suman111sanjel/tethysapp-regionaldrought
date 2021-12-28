<template>
  <div class="all-conts">
    <el-container class="cont-outer">
      <el-header>
        <NavBar></NavBar>
      </el-header>
      <el-container class="sidebar-main">
        <Tabs :activeTab="currentTab"></Tabs>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import NavBar from "../components/NavBar";
import Tabs from "../components/Tabs";

export default {
  name: "outlook",
  components: {
    NavBar,
    Tabs,
  },
  data() {
    return {
      selectedTab: 'outlook',
    };
  },
  computed: {
    currentTab() {
      return this.getCurrentTab()
    },
  },
  methods: {
    getCurrentTab() {
      return this.selectedTab;
    }
  }
};
</script>

<style lang="scss">
@import "../utils/main";

</style>
