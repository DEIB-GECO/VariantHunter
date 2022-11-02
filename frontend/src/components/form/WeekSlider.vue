<!--
  Component:    WeekSlider
  Description:  Slider for the analysis period

  Events:
  ├── moveBackward:  Emitted whenever prev button is pressed
  └── moveForward:   Emitted whenever next button is pressed
-->

<template>
  <v-col cols="12" class='d-flex'>
    <btn-with-tooltip bottom :click-handler="()=>$emit('moveBackward')" color="primary" text="Prev week"
                      icon="mdi-clock-minus-outline" tip="Shift the analysis period one week backward"/>
    <v-spacer></v-spacer>
    <btn-with-tooltip bottom :click-handler="()=>$emit('moveForward')" color="primary" append-icon text="Next week"
                      icon="mdi-clock-plus-outline" tip="Shift the analysis period one week forward"/>
  </v-col>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";

export default {
  name: 'WeekSlider',
  components: {BtnWithTooltip},
}

</script>
