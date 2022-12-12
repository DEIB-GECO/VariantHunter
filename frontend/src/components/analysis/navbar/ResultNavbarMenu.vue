<!--

  Component:    ResultNavbarMenu
  Description:  Toolbar menu option to show other options including
                an option to download data and an option to take a screenshot

-->

<template>
  <v-menu content-class="rounded-b-xl rounded-t-0 navbar-menu" offset-y open-on-hover v-model="visibility"
          :close-on-content-click="false">

    <!-- Activator: icon to open the option menu -->
    <template v-slot:activator="{ attrs, on }">
      <div v-bind="attrs" v-on="on">
        <v-btn icon>
          <v-icon color="primary">mdi-dots-horizontal</v-icon>
        </v-btn>
      </div>
    </template>

    <!-- Option menu content -->
    <v-list color="bg_var1" rounded dense>

      <!-- Download data option -->
      <download-data control-type="navbar" @click.native="hide"/>

      <!-- Take screenshot option -->
      <take-screenshot @click.native="hide"/>

      <!-- Share -->
      <result-navbar-share v-if="isPublicEndpoint" @click.native="hide(5000)"/>

    </v-list>

  </v-menu>
</template>

<script>
import DownloadData from "@/components/controls/DownloadData";
import TakeScreenshot from "@/components/controls/TakeScreenshot";
import ResultNavbarShare from "@/components/analysis/navbar/ResultNavbarShare.vue";
import {mapState} from "vuex";

export default {
  name: "ResultNavbarMenu",
  components: {ResultNavbarShare, TakeScreenshot, DownloadData},

  data() {
    return {
      /** Boolean visibility flag for the menu */
      visibility: false,
    }
  },

  methods: {
    /**
     * Hide the menu after a specified time
     * @param time  Delay in ms
     */
    hide(time) {
      if(time)
        setTimeout(() => {
          this.visibility = false
        }, time)
      else
        this.visibility = false
    }
  },

  computed: {
    ...mapState(['isPublicEndpoint'])
  }
}
</script>

<style scoped>

</style>