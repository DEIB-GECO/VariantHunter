<!--

  Component:    GoToCovSpectrum
  Description:  Table option to run an analysis on covSPECTRUM website

-->

<template>
  <div class="d-flex mt-4 px-5 width-100">
    <v-row no-gutters>
      <v-col class="text-center text-sm-left">

        <!-- Analysis generation action button -->
        <btn-with-tooltip size="small" :tip="showMenuOptions?'':undefined" outlined top color="primary"
                          :click-handler="()=>btnClickManager()">

          <!-- Custom appearance with covSPECTRUM logo -->
          <template v-slot:btn>
            <span ref="analyzeBtn">
              <v-icon left>mdi-open-in-new</v-icon>
              Analyze <span class="hidden-xs-only">the selected mutations</span> with
              <span class="pl-1 inline-img">
                <v-img max-height="14px" width="115px" contain :src="require('@/assets/others/CovSpecturm.svg')"/>
              </span>
            </span>

            <!-- Selection options menu-->
            <v-menu v-model="showMenuOptions" :attach="$refs.analyzeBtn" offset-y :position-y="23"
                    content-class="bg_var1 text-normal text-left" min-width="fill-available">
              <div class="break-spaces pt-4 px-4">You have selected multiple mutations. <br/>Choose how to select the
                sequences to be analyzed.
              </div>
              <v-list color="bg_var1" class="break-spaces" rounded dense width="auto">
                <v-list-item link dense @click="generateAnalysis(true)">
                  <v-icon class="pr-3" color="primary">mdi-set-all</v-icon>
                  <v-list-item-content>
                    <v-list-item-title class="primary--text">Use the <span class="font-weight-bold">OR</span> operator
                    </v-list-item-title>
                    <v-list-item-subtitle>Consider sequences that contain at least one of the selected mutations.
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link dense @click="generateAnalysis(false)">
                  <v-icon class="pr-3" color="primary">mdi-set-center</v-icon>
                  <v-list-item-content>
                    <v-list-item-title class="primary--text">Use the <span class="font-weight-bold">AND</span> operator
                    </v-list-item-title>
                    <v-list-item-subtitle>Considers only sequences that contain all of the selected mutations.
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>

              <!-- Compatibility warnings -->
              <div class="break-spaces pa-4 pt-0">
                <div class="mt-3 border-t error--text rounded-xl px-4 py-1" v-if="stopWarning">
                  <v-icon small color="error" left> mdi-alert</v-icon>
                  <span class="font-weight-bold">Warning:</span>
                  Stop mutations are not currently supported and will not be considered
                </div>
              </div>
            </v-menu>

          </template>

          <!-- Custom button user tip with a summary -->
          <template v-slot:tip>

            <!-- Feature intro/summary -->
            Run a search on <span class="font-weight-bold">covSPECTRUM</span> for the selected mutations and geographic
            area.
            <div class="mt-3 border-t" v-if="selectedRows.length<1">
              To begin, select the rows you are interested in from the table, then press this button.
            </div>
            <div class="mt-3 border-t" v-else>
              {{ selectedRows.length }} mutation<span v-if="selectedRows.length>1">s</span>&nbsp; selected. Press this
              button to proceed.
            </div>

            <!-- Compatibility warnings -->
            <div class="mt-3 border-t white--text  red rounded-xl px-4 py-1" v-if="stopWarning">
              <v-icon small color="white" left> mdi-alert</v-icon>
              <span class="font-weight-bold">Warning:</span>
              Stop mutations are not currently supported and will not be considered
            </div>

          </template>

        </btn-with-tooltip>

      </v-col>
    </v-row>
  </div>
</template>

<script>
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import {mapGetters} from "vuex";

export default {
  name: "GoToCovSpectrum",
  components: {BtnWithTooltip},

  data() {
    return {
      /** Boolean visibility flag for the menu options */
      showMenuOptions: false,
    }
  },

  computed: {
    ...mapGetters(['getCurrentAnalysis', 'getCurrentSelectedRows']),

    /** Currently selected rows of the table. Returns full row data. */
    selectedRows() {
      return this.getCurrentSelectedRows
    },

    /** Boolean flag set to true iff stop mutations have been selected */
    stopWarning() {
      return this.selectedRows.map(({mut}) => mut).find((mut) => mut.includes('stop')) !== undefined
    }
  },

  methods: {
    /** Manager for the click on 'analyze with covSpectrum' button */
    btnClickManager() {
      if (this.selectedRows.length > 1)
        this.showMenuOptions = true
      else
        this.generateAnalysis()
    },

    /**
     * Generate an analysis on covSPECTRUM for the selected parameters
     * @param useOr Boolean flag set to true if or operator should be used
     */
    generateAnalysis(useOr = true) {
      // Location data: if granularity is regional, then perform a country-level
      //                analysis since CovSpectrum does not support regions
      const {location: locationData, granularity} = this.getCurrentAnalysis.query
      const location = (granularity === 'region')
          ? locationData['country'].text
          : locationData[granularity].text

      // Period data: fetch the same period of the current analysis
      const endDate = this.getCurrentAnalysis.query.endDate
      let startDate = new Date(endDate)
      startDate.setDate(new Date(endDate).getDate() - 7)
      startDate = startDate.toISOString().slice(0, 10)

      // Selected mutations:  if present, format mutations query to be used in covSPECTRUM
      //                      as a string of converted concatenated mutations separated by +%7C+
      const muts = this.selectedRows
          .map(({protein, mut}) => this.convertFormat(protein, mut)) // converts
          .filter(str => str !== null) // remove unsupported muts
          .join(useOr ? '+%7C+' : '+%26+') // join to create the url

      // Finally generate the URL
      const url = "https://cov-spectrum.org/explore/" + location +
          "/AllSamples/from=" + startDate + "&to=" + endDate +
          "/variants" + (muts.length > 0 ? ("?variantQuery=" + muts) : "")
      window.open(url, '_blank').focus(); // open in new tab
    },

    /**
     * Convert GISAID protein notation into NEXTSTRAIN one.
     * It converts the protein into the correct one and possibly performs
     * changes to mut if the protein translation affects it
     * @param prot{string}   The protein name to be converted (e.g., 'Spike')
     * @param mut{string}    The mut name associated (e.g., 'L452R')
     * @returns {{prot:string, mut:string}}  The converted pair in the form {protein, mut}
     */
    convertProtein(prot, mut) {
      if (prot === "Spike") {
        // Spike => S
        return {prot: "S", mut}
      } else if (prot.startsWith("NSP")) {
        // Complex NSP to ORF translation
        return this.translateNSP(prot, mut)
      } else if (prot.startsWith("NS")) {
        // NS3 => ORF3a, otherwise NS<...> => ORF<...>
        return {prot: prot === 'NS3' ? ("ORF3a") : ("ORF" + prot.slice(2)), mut}
      } else {
        // No conversion required
        return {prot, mut}
      }
    },

    /**
     * Convert NSP protein into ORF.
     * The conversion affects also the mutation position
     * @param prot{string}  The protein name of the mutation to be converted (e.g., 'NSP3')
     * @param mut{string}   The mutation to be converted (e.g., 'L452R')
     * @returns {{prot:string, mut:string}}   The converted pair in the form {protein, mut}
     */
    translateNSP(prot, mut) {
      const coords = {
        'ORF1a': [266, 13468],
        'ORF1b': [13468, 21555],
        'NSP1': [266, 805],
        'NSP2': [806, 2719],
        'NSP3': [2720, 8554],
        'NSP4': [8555, 10054],
        'NSP5': [10055, 10972],
        'NSP6': [10973, 11842],
        'NSP7': [11843, 12091],
        'NSP8': [12092, 12685],
        'NSP9': [12686, 13024],
        'NSP10': [13025, 13441],
        'NSP11': [13442, 13480],
        'NSP12': [13442, 16236],
        'NSP13': [16237, 18039],
        'NSP14': [18040, 19620],
        'NSP15': [19621, 20658],
        'NSP16': [20659, 21552]
      }

      let [, ref, pos, alt,] = mut.match(/([a-zA-Z]+)(\d+)([a-zA-Z]+)/)
      pos = parseInt(pos)
      const start = coords[prot][0]  // current protein start position

      const newPosNucleotides = start + pos * 3 // nucleotides pos
      const startORF1b = coords['ORF1b'][0]
      let newPosNucleotidesWrtORF, newPosAminoacidsWrtORF

      if (newPosNucleotides > startORF1b) {
        // ORF1b case
        prot = 'ORF1b'
        newPosNucleotidesWrtORF = newPosNucleotides - startORF1b
        newPosAminoacidsWrtORF = Math.floor(newPosNucleotidesWrtORF / 3)
      } else {
        // ORF1a case
        prot = 'ORF1a'
        const startORF1a = coords['ORF1a'][0]
        newPosNucleotidesWrtORF = newPosNucleotides - startORF1a
        newPosAminoacidsWrtORF = Math.floor(newPosNucleotidesWrtORF / 3)
      }

      return {
        prot: prot,
        mut: ref.concat(String(newPosAminoacidsWrtORF)).concat(alt)
      }
    },

    /**
     * Convert GISAID mutation notation into NEXTSTRAIN one.
     * This step of conversion is related to ins and del
     * @param prot{string}   The protein name to be converted (e.g., 'Spike')
     * @param mut{string}    The mut name associated (e.g., 'L452del')
     * @returns {string}     The final string
     */
    convertMutation(prot, mut) {
      const separator = '%3A' // protein-mutation separator code (escape code of ':')

      if (mut.startsWith('ins')) {
        // ins214EPE => ins_S:214:EPE
        mut = mut.slice(3) // 214EPE
        return 'ins_' + prot + separator + mut.match(/\d+/) + separator + mut.match(/\D+/)
      } else if (mut.endsWith('del')) {
        // Spike_V70del => S:V70-
        mut = mut.slice(0, -3) // V70
        return prot + separator + mut + '-'
      } else {
        // Regular conversion case
        return prot + separator + mut
      }
    },

    /**
     * Convert GISAID notation into NEXTSTRAIN one
     * The conversion is based on the actual value of the string.
     * @param prot{string}    The protein name of the format to be converted (e.g., 'Spike')
     * @param mut{string}     The mutation of the format to be converted (e.g., 'L452R')
     * @returns {string|null} Either the converted string or null if the mutation is currently not supported
     */
    convertFormat(prot, mut) {
      // Not supported mutation? return null
      if (!this.isSupportedMut(prot, mut)) return null

      // First level conversion
      let {prot:newProt, mut:newMut} = this.convertProtein(prot, mut)

      // Second level conversion
      return this.convertMutation(newProt, newMut)
    }
    ,

    /**
     * CovSpectrum compatibility check
     * Given a protein and a mutation checks whether it is currently
     * supported by the converter
     * @param protein The protein name of the format to be converted (e.g., 'Spike')
     * @param mut     The mutation of the format to be converted (e.g., 'L452R')
     * @returns {boolean}  True iff the mutation is NOT a stop mutation
     */
    isSupportedMut(protein, mut) {
      return !mut.includes('stop')
    }
  },
}
</script>

<style>
#app .inline-img .v-image {
  display: inline-block !important;
}
</style>