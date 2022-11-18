<template>
  <v-menu v-model="showOptions" content-class="rounded-b-xl rounded-t-0 navbar-menu" offset-y open-on-click
          :open-on-hover="false" close-on-content-click>
    <template v-slot:activator="{ attrs, on }">
      <div v-bind="attrs" v-on="on">
        <icon-with-tooltip hover-color="success" icon="mdi-clock-edit-outline"
                           :tip="showOptions?'':'Shift the analysis period backward or forward'" bottom
                           :click-handler="()=>showOptions=!showOptions" color="primary"/>
      </div>
    </template>
    <div @mouseleave="showOptions=false">
      <v-list color="bg_var1" rounded dense width="auto">
        <v-list-item link dense v-for="(opt,idx) in options" :key="idx" @click="$emit('shiftPeriod',opt.delta)">
          <v-icon class="pr-3" color="primary">

            {{ (opt.type === 'forward') ? 'mdi-sort-clock-ascending-outline' : 'mdi-sort-clock-descending-outline' }}
          </v-icon>
          <v-list-item-content>
            <v-list-item-title class="primary--text">{{ opt.label }}&nbsp;<span class="font-weight-black">{{ opt.type }}</span></v-list-item-title>
            <v-list-item-subtitle>Shift analysis period {{ opt.label }}&nbsp;{{ opt.type }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </div>
  </v-menu>
</template>

<script>
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "ResultNavbarWeekSlider",
  components: {IconWithTooltip},
  data() {
    return {
      showOptions: false,

      options: [
        {delta: -14, type: 'backward', label: '2 weeks'},
        {delta: -7, type: 'backward', label: '1 week'},
        {delta: +7, type: 'forward', label: '1 week'},
        {delta: +14, type: 'forward', label: '2 weeks'},
      ]
    }
  }
}
</script>

<style scoped>

</style>