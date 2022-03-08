<!--
  Component:    DialogOpener
  Description:  Button that opens a v-dialog.

  Props:
  ├── title:  Title for the dialog. Required.
  └── icon:  Icon for the dialog.

  Slots:
  └── default:  The content of the dialog
-->

<template>

  <v-flex class="xs12 sm6 md3 d-flex" justify-center>

    <!-- Dialog opener -->
    <v-btn color="primary" depressed outlined rounded small @click="showDialog=true">
      <v-icon left>{{ icon }}</v-icon>
      <div v-if="buttonPrefix">Show&nbsp;</div>
      {{ title }}
    </v-btn>

    <!-- Dialog element-->
    <v-dialog v-model="showDialog" max-width="850" transition="dialog-bottom-transition">
      <v-card>

        <!-- Dialog title -->
        <v-toolbar :color="primary_color" class="dialog-title" dark flat>
          <v-icon left>mdi-help-circle-outline</v-icon>
          {{ title }}
        </v-toolbar>

        <!-- Dialog content -->
        <v-card-text class="text-s-center dialog-text">
          <slot>
          </slot>
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
import {mapState} from "vuex";

export default {
  name: "DialogOpener",
  props: {

    /** Title for the dialog. Required */
    title: {
      required: true
    },

    /** Icon for the dialog. */
    icon: {default: "mdi-help-circle-outline"},

    /* FLag to add the prefix "show" on the button */
    buttonPrefix: {default: true}

  },
  data() {
    return {

      /** Flag to show the dialog element */
      showDialog: false,

    }
  },
  computed: {
    ...mapState(['primary_color']),
  }
}
</script>

<style scoped>

/* Header info dialog styling*/
.dialog-title {
  text-transform: uppercase;
  font-weight: 600;
  font-size: 20px;
}

</style>

<style>

/* Global style fot the content of the dialog */
.dialog-text ul {
  margin-top: 40px;
}

.dialog-text li {
  font-size: 16px;
  padding-bottom: 10px;
}
</style>