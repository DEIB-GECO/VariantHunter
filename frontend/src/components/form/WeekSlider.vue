<!--

  Component:    WeekSlider
  Description:  Slider for the analysis period

  Events:
  └── shiftPeriod:   Emitted whenever next/prev buttons are pressed together with the delay

-->

<template>
  <v-row class="mt-8">
    <v-col cols="12" class='d-flex'>
      <btn-with-tooltip bottom :click-handler="()=>$emit('shiftPeriod',-7)" color="primary" text="Prev week"
                        content-class="text_var2--text"
                        icon="mdi-sort-clock-descending-outline" tip="Shift the analysis period 1 week backward"/>
      <v-spacer></v-spacer>
      <btn-with-tooltip bottom :click-handler="()=>$emit('shiftPeriod',+7)" color="primary" append-icon text="Next week"
                        content-class="text_var2--text"
                        icon="mdi-sort-clock-ascending-outline" tip="Shift the analysis period 1 week forward"/>
    </v-col>
  </v-row>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";

export default {
  name: 'WeekSlider',
  components: {BtnWithTooltip},
}

</script>
