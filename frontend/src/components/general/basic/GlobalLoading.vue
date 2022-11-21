<template>
  <v-dialog v-model="loading" hide-overlay persistent>
    <v-overlay :value="true" color="primary" opacity="0.9" class="loading-global">
      <v-list class="text-left transparent tip rounded-xl warning--text mx-5" two-line>
      <v-list-item class="justify-center">
          <v-list-item-icon class="text-center ma-auto mr-8">
            <v-progress-circular color="warning" indeterminate/>
          </v-list-item-icon>
          <v-list-item-content>
            <div class="text-h5 compact-text-0 font-weight-bold">
              Loading...
            </div>
            <v-list-item-subtitle class="text-body-3">
              Please wait
            </v-list-item-subtitle>

          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-progress-linear height="10px" color="warning" indeterminate/>
    </v-overlay>
  </v-dialog>

</template>

<script>
import {mapState} from "vuex";

export default {
  name: "GlobalLoading",
  computed:{
    ...mapState(['loading']),
  }
}
</script>

<style scoped>
.loading-global{
 margin-top: 56px;
  border-radius: 0;
}
</style>