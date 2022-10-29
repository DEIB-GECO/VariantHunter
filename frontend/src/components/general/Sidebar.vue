<template>
  <v-navigation-drawer class="sidebar-sizing" :mini-variant="isCollapsed" clipped permanent @update:mini-variant="onCollapse" expand-on-hover
                       absolute dark color="primary" width="500px" >
    <div ref="el"></div>
    <v-list rounded nav dense>
      <list-item icon="mdi-plus" title="New analysis" link subtitle="Perform a new analysis" expand-on-hover/>
      <v-divider/>

      <list-item icon="mdi-history" title="Recent analysis" subtitle="Your recent analysis" with-actions>
        <template v-slot:actions>
          <icon-with-tooltip v-if="showHistory" icon="mdi-chevron-up" tip="Collapse" bottom :click-handler="()=>{showHistory=false}"/>
          <icon-with-tooltip v-else icon="mdi-chevron-down" tip="Expand" bottom :click-handler="()=>{showHistory=true}"/>
        </template>
      </list-item>
      <v-expand-transition>
        <search-history v-if="showHistory" type="all"/>
      </v-expand-transition>

    </v-list>
  </v-navigation-drawer>
</template>

<script>
import ListItem from "@/components/general/basic/ListItem";
import SearchHistory from "@/components/general/SearchHistory";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "Sidebar",
  components: {IconWithTooltip, SearchHistory, ListItem},
  data() {
    return {
      showSidebar: true,
      isCollapsed: true,
      showHistory:true,
    }
  },
  methods:{
    onCollapse(){
    }
  }
}
</script>

<style scoped>
.sidebar-sizing {
  max-width: 90vw !important;
}
</style>