<template>
  <v-menu content-class="rounded-b-xl rounded-t-0 navbar-menu" offset-y open-on-hover>
    <template v-slot:activator="{ attrs, on }">
      <div v-bind="attrs" v-on="on">
        <v-btn icon>
          <v-icon color="primary">mdi-dots-horizontal</v-icon>
        </v-btn>
      </div>
    </template>

    <v-list color="bg_var1" rounded dense>
      <download-data control-type="navbar"/>
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