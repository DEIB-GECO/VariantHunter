<template>
  <div class="d-flex mt-4 px-5 width-100">
    <v-row no-gutters><v-col class="text-center text-sm-left">
    <btn-with-tooltip size="small" outlined top color="primary" :click-handler="generateAnalysis">

      <template v-slot:btn>
        <v-icon left>mdi-open-in-new</v-icon>
        Analyze <span class="hidden-xs-only">the selected mutations</span> with
        <span class="pl-1 inline-img">
          <v-img max-height="14px" width="115px" contain :src="require('@/assets/others/CovSpecturm.svg')"/>
        </span>
      </template>

      <template v-slot:tip>
        Run a search on <span class="font-weight-bold">covSPECTRUM</span> for the selected mutations and geographic
        area.
        <div class="mt-3 border-t" v-if="selectedRows.length<1">
          To begin, select the rows you are interested in from the table, then press this button.
        </div>
        <div class="mt-3 border-t" v-else>
          {{ selectedRows.length }} mutation<span v-if="selectedRows.length>1">s</span>&nbsp; selected. Press this button to proceed.
        </div>
        <div class="mt-3 border-t white--text  red rounded-xl px-4 py-1" v-if="nspWarning">
          <v-icon small color="white" left> mdi-alert</v-icon>
          <span class="font-weight-bold">Warning:</span>
          NSP proteins are not currently supported and will not be considered
        </div>
        <div class="mt-3 border-t white--text  red rounded-xl px-4 py-1" v-if="stopWarning">
          <v-icon small color="white" left> mdi-alert</v-icon>
          <span class="font-weight-bold">Warning:</span>
          Stop mutations are not currently supported and will not be considered
        </div>


      </template>

    </btn-with-tooltip>
    </v-col></v-row>
  </div>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import {mapGetters} from "vuex";

export default {
  name: "GoToCovSpectrum",
  components: {BtnWithTooltip},
  computed:{
    ...mapGetters(['getCurrentAnalysis','getCurrentSelectedRows']),

    selectedRows(){
      return this.getCurrentSelectedRows
    },

    /** True iff NSP proteins have been selected */
    nspWarning(){
      return this.selectedRows.map(({protein})=>protein).find((protein)=>protein.startsWith('NSP')) !== undefined
    },

    /** True iff stop mutations have been selected */
    stopWarning(){
      return this.selectedRows.map(({mut})=>mut).find((mut)=>mut.includes('stop')) !== undefined
    }
  },
  methods: {
    generateAnalysis() {
      // If granularity is regional, then perform a country-level analysis since CovSpectrum does not support regions
      const {location:locationData, granularity}=this.getCurrentAnalysis.query
      const location = granularity === 'region'
          ? locationData['country'].text
          : locationData[granularity].text

      const endDate = this.getCurrentAnalysis.query.endDate
      let startDate = new Date(endDate)
      startDate.setDate(new Date(endDate).getDate() - 7)
      startDate = startDate.toISOString().slice(0, 10)

      // Format mutations query
      const muts = this.selectedRows
          .map(({protein, mut}) => this.convertFormat(protein,mut)) // converts
          .filter(str => str!==null) // remove unsupported muts
          .join('+%7C+') // join to create the url

      const url = "https://cov-spectrum.org/explore/" + location +
          "/AllSamples/from=" + startDate + "&to=" + endDate +
          "/variants" + (muts.length > 0 ? ("?variantQuery=" + muts) : "")
      window.open(url, '_blank').focus();
    },

    /**
     * Convert GISAID protein notation into NEXTSTRAIN one
     */
    getProtein(protein) {
      if (protein === "Spike") {
        return "S"
      } else if (protein.startsWith("NS")) {
        return protein==='NS3'? ("ORF3a"):("ORF"+protein.slice(2))
      } else {
        return protein
      }
    },

    /**
     * Convert GISAID mutation notation into NEXTSTRAIN one
     */
    getMut(protein,mut) {
      if(protein==='NS'){
        return mut.slice(1)
      }else{
        return mut
      }
    },

    /**
     * Convert GISAID notation into NEXTSTRAIN one
     */
    convertFormat(protein,mut) {
      if(!this.isSupportedMut(protein,mut))  return null

      // Actual conversion process
      const separator='%3A'

      if (mut.startsWith('ins')) {
        // ins214EPE => ins_S:214:EPE
        mut = mut.slice(3)
        return 'ins_'+ this.getProtein(protein) + separator + mut.match(/\d+/) + separator + mut.match(/\D+/)
      } else if (mut.endsWith('del')) {
        // Spike_V70del => S:V70-
        return this.getProtein(protein) + separator + mut.slice(0, -3) + '-'
      } else {
        return this.getProtein(protein) + separator + this.getMut(protein,mut)
      }
    },

    /**
     * CovSpectrum compatibility check
     */
    isSupportedMut(protein, mut) {
      return (!mut.includes('stop') && !protein.startsWith('NSP'))
    }
  }
}
</script>

<style>
#app .inline-img .v-image{
  display: inline-block !important;
}
</style>