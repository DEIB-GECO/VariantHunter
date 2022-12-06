<!--

  Component:    ResultNavbarMenu
  Description:  Toolbar menu option to show other options including
                an option to download data and an option to take a screenshot

-->

<template>
  <v-menu content-class="rounded-b-xl rounded-t-0 navbar-menu" offset-y open-on-hover>

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
      <download-data control-type="navbar"/>

      <!-- Take screenshot option -->
      <take-screenshot/>

    </v-list>

  </v-menu>
</template>

<script>
import DownloadData from "@/components/controls/DownloadData";
import TakeScreenshot from "@/components/controls/TakeScreenshot";

export default {
  name: "ResultNavbarMenu",
  components: {TakeScreenshot, DownloadData}
}
</script>

<style scoped>

</style>