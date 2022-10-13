<template>
  <v-card width="90%" class="options text-left" color="transparent" flat>
    <div class="options-intro">
      <div class="main">Lineages breakdown </div>
      computed considering {{expansionMode===0?'this line':'the entire dataset'}}
    </div>
    <MenuButton icon="mdi-pencil" text="Change scope" :options="scopeOptions" @select="e=>expansionMode=e"/>
    <MenuButton icon="mdi-code-string" :text="(notationMode===0?'Simplify':'Expand') +' notation'" :options="notationOptions" @select="e=>notationMode=e"/>
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
          description:'Differentiate each lineage (e.g.: BA.1, BA.2,...) by avoiding groupings.',
          icon:'mdi-text-long'},
        { value:1,
          text:'Use simplified notation',
          description:'Summarize the counts using a star notation for the lineages (e.g.: BA.*,...).',
          icon:'mdi-minus'}
      ]
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