<template>
  <v-menu v-if="!isContinental" v-model="showOptions" content-class="rounded-b-xl rounded-t-0 navbar-menu" offset-y open-on-click
          :open-on-hover="false" close-on-content-click>
    <template v-slot:activator="{ attrs, on }">
      <div v-bind="attrs" v-on="on">
        <icon-with-tooltip hover-color="success" icon="mdi-airplane-edit"
                           :tip="showOptions?'':'Change granularity level'" bottom
                           :click-handler="()=>showOptions=!showOptions" color="primary"/>
      </div>
    </template>
    <div @mouseleave="showOptions=false">
      <v-list color="bg_var1" rounded dense width="auto">
        <v-list-item link dense @click="$emit('shiftArea',continent)">
          <v-icon class="pr-3" color="primary">mdi-earth</v-icon>
          <v-list-item-content>
            <v-list-item-title class="primary--text">Switch to&nbsp;<span class="font-weight-black">{{continent.text}}</span></v-list-item-title>
            <v-list-item-subtitle>Run continental analysis</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="!isNational" link dense @click="$emit('shiftArea',country)">
          <v-icon class="pr-3" color="primary">mdi-map-outline</v-icon>
          <v-list-item-content>
            <v-list-item-title class="primary--text">Switch to&nbsp;<span class="font-weight-black">{{country.text}}</span></v-list-item-title>
            <v-list-item-subtitle>Run national analysis</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </div>
  </v-menu>
</template>

<script>
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import {mapGetters} from "vuex";

export default {
  name: "ResultNavbarLocationSwitcher",
  components: {IconWithTooltip},
  data() {
    return {
      showOptions: false,
    }
  },
  computed: {
    ...mapGetters(['getCurrentAnalysis']),

    isContinental(){
      return this.getCurrentAnalysis.query.granularity==='continent'
    },

    isNational(){
      return this.getCurrentAnalysis.query.granularity==='country'
    },

    continent(){
      return this.getCurrentAnalysis.query.location.continent
    },

    country(){
      return this.getCurrentAnalysis.query.location.country
    },
  }
}
</script>

<style scoped>

</style>