<!--

  Component:    ResultNavbarLocationSwitcher
  Description:  Toolbar option to switch location to higher level granularities

  Events:
  └── shiftArea:  Emitted on location switch together with the new location data (id and text)

-->

<template>
  <v-menu v-if="!isContinental" v-model="showOptions" content-class="rounded-b-xl rounded-t-0 navbar-menu" offset-y
          open-on-click
          :open-on-hover="false" close-on-content-click>

    <!-- Activator: icon to open the option menu -->
    <template v-slot:activator="{ attrs, on }">
      <div v-bind="attrs" v-on="on">
        <icon-with-tooltip hover-color="success" icon="mdi-airplane-edit"
                           :tip="showOptions?'':'Change granularity level'" bottom
                           :click-handler="()=>showOptions=!showOptions" color="primary"/>
      </div>
    </template>

    <!-- Option menu content -->
    <div @mouseleave="showOptions=false">
      <v-list color="bg_var1" rounded dense width="auto">

        <!-- Shift to continental analysis -->
        <v-list-item link dense @click="$emit('shiftArea',continent)">
          <v-icon class="pr-3" color="primary">mdi-earth</v-icon>
          <v-list-item-content>
            <v-list-item-title class="primary--text">Switch to&nbsp;<span
                class="font-weight-black">{{ continent.text }}</span></v-list-item-title>
            <v-list-item-subtitle>Run continental analysis</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <!-- Shift to national analysis -->
        <v-list-item v-if="!isNational" link dense @click="$emit('shiftArea',country)">
          <v-icon class="pr-3" color="primary">mdi-map-outline</v-icon>
          <v-list-item-content>
            <v-list-item-title class="primary--text">Switch to&nbsp;<span
                class="font-weight-black">{{ country.text }}</span></v-list-item-title>
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
      /** Boolean visibility flag of options menu **/
      showOptions: false,
    }
  },

  computed: {
    ...mapGetters(['getCurrentAnalysis']),

    /** Boolean flag set to true if the current granularity is continent */
    isContinental() {
      return this.getCurrentAnalysis.query.granularity === 'continent'
    },

    /** Boolean flag set to true if the current granularity is country */
    isNational() {
      return this.getCurrentAnalysis.query.granularity === 'country'
    },

    /** Continent data (including id and text) of the current analysis */
    continent() {
      return this.getCurrentAnalysis.query.location.continent
    },

    /** Country data (including id and text) of the current analysis */
    country() {
      return this.getCurrentAnalysis.query.location.country
    },
  }
}
</script>

<style scoped>

</style>