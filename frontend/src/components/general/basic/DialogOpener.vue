<!--
  Component:    DialogOpener
  Description:  Button that opens a v-dialog.

  Props:
  ├── title:          Title for the dialog. Required.
  ├── icon:           Icon for the dialog.
  └── buttonPrefix:   Flag to add the prefix "show" on the button

  Slots:
  └── default:  The content of the dialog
-->

<template>
  <v-flex class="d-flex pa-1" justify-center>

    <!-- Dialog opener -->
    <v-btn :color='color' depressed outlined rounded small @click='showDialog = true'>
      <v-icon left>{{ icon }}</v-icon>
      <div v-if='buttonPrefix'>Show&nbsp;</div>
      <span v-html="title"></span>
    </v-btn>

    <!-- Dialog element-->
    <v-dialog v-model="showDialog" max-width="850" transition="dialog-bottom-transition">
      <v-card>
        <!-- Dialog title -->
        <v-toolbar color="f_primary" class="dialog-title" dark flat>
          <v-icon left large>mdi-help-circle-outline</v-icon>
          <span v-html="title"></span>
        </v-toolbar>

        <!-- Dialog content -->
        <v-card-text class="text-s-center dialog-text">
          <slot></slot>
        </v-card-text>

        <!-- Dialog actions -->
        <v-card-actions class="justify-end">
          <v-btn text @click="showDialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-flex>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'DialogOpener',
  props: {
    /** Title for the dialog. Required */
    title: { required: true },

    /** Icon for the dialog. */
    icon: { default: 'mdi-help-circle-outline' },

    /* Flag to add the prefix "show" on the button */
    buttonPrefix: { default: true },

    color:{default:'f_primary'},
  },
  data () {
    return {
      /** Flag to show the dialog element */
      showDialog: false
    }
  }
}
</script>

<style>
/* Header info dialog styling*/
.dialog-title {
  text-transform: uppercase !important;
  font-weight: 600 !important;
  font-size: 20px !important;
}

/* Global style fot the content of the dialog */
.dialog-text {
  padding-top: 10px !important;
  font-size: 16px !important;
}

.dialog-text p:first-child{
  padding-top: 15px;
}

.ul-table{
  display: flex;
  flex-direction: column;
}

.li-table{
  padding-top: 10px;
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: solid 1px var(--tertiary-color-light);
  display: flex;
  flex-direction: row;
}

.li-name{
  width: 20%;
  min-width: 100px;
  font-weight: bold;
  padding-right: 5px;
  margin-right: 20px;
  border-right: solid 1px var(--tertiary-color-light);
}

.li-content{
  width: 80%;
}
</style>
