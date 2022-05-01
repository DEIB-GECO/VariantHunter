<!--
  Component:    WeekSlider
  Description:  Slider for the analysis period

  Events:
  ├── moveBackward:  Emitted whenever prev button is pressed
  └── moveForward:   Emitted whenever next button is pressed
-->

<template>
  <v-flex class='xs12 d-flex'>
    <v-tooltip right max-width='400' color='white' open-delay='0'>
      <template v-slot:activator='{ on, attrs }'>
        <v-btn v-bind='attrs' v-on='on' class='white--text' :color='primary_color'
               @click="$emit('moveBackward' )" depressed>
          <v-icon left>mdi-chevron-left</v-icon>
          PREV WEEK
        </v-btn>
      </template>
      <div class='tooltip'>
        Shift the analysis one week <b>backward</b>.
        <div class='additional-info'>
        This will keep the values of the filtering options and also the mutations
        selected in the table (if still present).
        </div>
      </div>
    </v-tooltip>

    <v-spacer></v-spacer>

    <v-tooltip left max-width='400' color='white' open-delay='0'>
      <template v-slot:activator='{ on, attrs }'>
        <v-btn v-bind='attrs' v-on='on' class='white--text' :color='primary_color'
               @click="$emit('moveForward' )" depressed>
          NEXT WEEK
        <v-icon right>mdi-chevron-right</v-icon>
        </v-btn>
      </template>
      <div class='tooltip'>
        Shift the analysis one week <b>forward</b>.
        <div class='additional-info'>
        This will keep the values of the filtering options and also the mutations
        selected in the table (if still present).
        </div>
      </div>
    </v-tooltip>
  </v-flex>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'WeekSlider',
  computed: {
    ...mapState(['primary_color'])
  }
}
</script>

<style scoped>

.tooltip{
  color: rgb(68, 68, 68);
  text-align: center;
}

.additional-info{
  margin-top: 3px;
  text-transform: uppercase;
  font-size: 11px;
  line-height: 13px;
}

</style>
