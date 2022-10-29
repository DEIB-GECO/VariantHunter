<!--
  View:         HomeView
  Description:  View container for the tool home
-->
<template>
  <div>

    <Sidebar/>
    <div class="tool-views-container">{{this.$store.state.currentAnalysis}} </div>

  </div>
</template>

<script>
import Sidebar from "@/components/general/Sidebar";
export default {
  name: "HomeView",
  components: {Sidebar},
  data(){
    return {
    }
  }
}
</script>

<style scoped>
.tool-views-container{
  margin-left: 56px;
}
</style>