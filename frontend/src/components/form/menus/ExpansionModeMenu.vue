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
      <div class="main">Lineages breakdown </div>
      computed considering {{expansionMode===0?'this line':'the entire dataset'}}
    </div>
    <MenuButton icon="mdi-pencil" text="Change scope" :options="scopeOptions" @select="expansionModeManager"/>
    <MenuButton icon="mdi-code-string" :text="'Change notation'" :options="notationOptions" @select="notationModeManager"/>
  </v-card>
</template>

<script>
import MenuButton from "@/components/form/menus/MenuButton";
export default {
  name: "ExpansionModeMenu",
  components: {MenuButton},
  data(){
    return{
      expansionMode:0,
      scopeOptions:[
        { value:0,
          text:'Consider this line only',
          description:'Compute the diffusion of each lineage considering the expanded line only.',
          icon:'mdi-city-variant-outline'},
        { value:1,
          text:'Consider the entire dataset',
          description:'Compute the diffusion of each lineage considering the whole dataset (ever and everywhere).',
          icon:'mdi-earth'}
      ],

      notationMode:0,
      notationOptions:[
        { value:0,
          text:'Use complete notation',
          description:'Differentiate each lineage (e.g.: B.1.1, B.1.2,...) by avoiding groupings.',
          icon:'mdi-text-long'},
        { value:1,
          text:'Use simplified notation',
          description:'Summarize the counts using a star notation for the lineages (e.g.: B.1.*,...).',
          icon:'mdi-minus'}
      ]
    }
  },
  methods:{
    expansionModeManager(e){
      this.expansionMode=e
      this.$emit('changeExpansionMode',e)
    },

    notationModeManager(e){
      this.notationMode=e
      this.$emit('changeNotationMode',e)
    }
  }
}
</script>

<style scoped>
.options{
  padding-left: 35px;
  position: absolute;
  top: 0;
}

.options-intro{
  padding-top: 13px;
  margin-bottom: 10px;
  color: rgba(0, 0, 0, 0.6);
  font-weight: normal;
  font-size: 12px;
  line-height: 13px;
  letter-spacing: 0.019em;
}
.options-intro .main{
  font-weight: bold;
}
</style>