<!--
  Component:    ExpasionModeMenu
  Description:  Component to change modes for the expanded row

  Props:
  ├── queryResult:  Array of raw data fetched from the server
  ├── queryParams:  Object storing the query parameters {granularity, location, date, [lineage]}
  ├── querySupport: Object storing additional info such as total number of sequences collected per week and characterizing muts
  ├── queryCustOpt: Object storing the custom preselection for the filtering/selection options
  └── withLineages: Lineages flag. True if the data refers to a lineage specific analysis.

  Events:
  ├── askAnalysis:  Emitted whenever a next/prev button is pressed
  └── error:        Emitted on server errors
-->

<template>
  <v-card width="90%" class="options text-left" color="transparent" flat>
    <div class="options-intro">
      <div class="main">Lineages breakdown</div>
      computed considering the expanded mutation in the 4 weeks and location
    </div>
    <v-menu v-model="showOptions" content-class="rounded-xl navbar-menu" offset-y open-on-click width="250px" max-width="80vw"
            :open-on-hover="false" close-on-content-click>
      <template v-slot:activator="{ attrs, on }">
                  <span v-bind="attrs" v-on="on">
                    <btn-with-tooltip bottom color="primary" outlined hover-color="warning" size="x-small"
                                      :icon="notationOptions[notationMode].icon" text="Change notation"
                                      :tip="showOptions?'':'Change the notation for the lineages by defining the level of aggregation'"
                                      :click-handler="()=>showOptions=!showOptions"/>
                  </span>
      </template>
      <div @mouseleave="showOptions=false">
        <v-list color="bg_var1" rounded dense width="auto">
          <v-list-item v-for="[key,opt] in Object.entries(notationOptions)" :key="key" link dense
                       @click="changeNotationMode(key)" :class="(key===notationMode)?'v-list-item--active':''">
            <v-icon class="pr-3" color="primary">{{ opt.icon }}</v-icon>
            <v-list-item-content>
              <v-list-item-title class="primary--text">{{ opt.text }}</v-list-item-title>
              <v-list-item-subtitle v-html="opt.description" class="break-spaces"/>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
    </v-menu>
  </v-card>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";

export default {
  name: "ExpansionModeMenu",
  components: {BtnWithTooltip},
  props:{
    value:{},
  },
  data() {
    return {
      showOptions: false,

      notationOptions: {
        1: {
          text: 'Use simplified notation (level 1)',
          description: 'Summarize the counts using a level-1 star notation for the lineages (e.g., B.1.*). <br/>' +
              'In any case, lineages exceeding 10% spread will not be aggregated',
          icon: 'mdi-minus'
        },
        2: {
          text: 'Use simplified notation (level 2)',
          description: 'Summarize the counts using a level-2 star notation for the lineages (e.g., B.1.1.*). <br/>' +
              'In any case, lineages exceeding 10% spread will not be aggregated',
          icon: 'mdi-equal'
        },
        0: {
          text: 'Use complete notation',
          description: 'Differentiate each lineage (e.g.: B.1.1, B.1.2,...) by avoiding groupings.',
          icon: 'mdi-text-long'
        },
      }
    }
  },
  computed:{
    notationMode:{
      set(newVal){
        this.$emit('input',Number(newVal))
      },
      get(){
        return String(this.value)
      }
    },
  },
  methods: {

    changeNotationMode(e) {
      this.notationMode = e
    }
  }
}
</script>

<style scoped>
.options {
  padding-left: 35px;
  position: absolute;
  top: 0;
}

.options-intro {
  max-width: 170px;
  padding-top: 13px;
  margin-bottom: 10px;
  color: var(--v-text_var1-base);
  font-weight: normal;
  font-size: 12px;
  line-height: 13px;
  letter-spacing: 0.019em;
}

.options-intro .main {
  font-weight: bold;
}
</style>