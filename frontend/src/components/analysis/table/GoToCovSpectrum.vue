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
              <v-list color="bg_var1" rounded dense width="auto">
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
                <div class="mt-0 border-t error--text rounded-xl px-4 py-1" v-if="nspWarning">
                  <v-icon small color="error" left> mdi-alert</v-icon>
                  <span class="font-weight-bold">Warning:</span>
                  NSP proteins are not currently supported and will not be considered
                </div>
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
      showMenuOptions: true
    }
  },

  computed: {
    ...mapGetters(['getCurrentAnalysis', 'getCurrentSelectedRows']),

    /** Currently selected rows of the table. Returns full row data. */
    selectedRows() {
      return this.getCurrentSelectedRows
    },

    /** Boolean flag set to true iff NSP proteins have been selected */
    nspWarning() {
      return this.selectedRows.map(({protein}) => protein).find((protein) => protein.startsWith('NSP')) !== undefined
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
     * The conversion is based on the actual value of the string.
     * @param protein The protein name to be converted (e.g., 'Spike')
     * @returns {*|string|string} The converted protein string
     */
    getProtein(protein) {
      if (protein === "Spike") {
        // Spike => S
        return "S"
      } else if (protein.startsWith("NS")) {
        // NS3 => ORF3a, otherwise NS<...> => ORF<...>
        return protein === 'NS3' ? ("ORF3a") : ("ORF" + protein.slice(2))
      } else {
        // No conversion required
        return protein
      }
    },

    /**
     * Convert GISAID mutation notation into NEXTSTRAIN one
     * The conversion is based on the actual value of the string.
     * @param protein The protein name of the mutation to be converted (e.g., 'Spike')
     * @param mut     The mutation to be converted (e.g., 'L452R')
     * @returns {*} The
     */
    getMut(protein, mut) {
      if (protein === 'NS') {
        return mut.slice(1) // probably useless
      } else {
        return mut
      }
    },

    /**
     * Convert GISAID notation into NEXTSTRAIN one
     * The conversion is based on the actual value of the string.
     * @param protein The protein name of the format to be converted (e.g., 'Spike')
     * @param mut     The mutation of the format to be converted (e.g., 'L452R')
     * @returns {string|null} Either the converted string or null if the mutation is currently not supported
     */
    convertFormat(protein, mut) {
      // Not supported mutation? return null
      if (!this.isSupportedMut(protein, mut)) return null

      /** Actual conversion process **/
      const separator = '%3A' // protein-mutation separator code (escape code of ':')

      // Handle special complex conversion cases
      if (mut.startsWith('ins')) {
        // ins214EPE => ins_S:214:EPE
        mut = mut.slice(3) // 214EPE
        return 'ins_' + this.getProtein(protein) + separator + mut.match(/\d+/) + separator + mut.match(/\D+/)
      } else if (mut.endsWith('del')) {
        // Spike_V70del => S:V70-
        return this.getProtein(protein) + separator + mut.slice(0, -3) + '-'
      } else {
        // Regular conversion case
        return this.getProtein(protein) + separator + this.getMut(protein, mut)
      }
    },

    /**
     * CovSpectrum compatibility check
     * Given a protein and a mutation checks whether it is currently
     * supported by the converter
     * @param protein The protein name of the format to be converted (e.g., 'Spike')
     * @param mut     The mutation of the format to be converted (e.g., 'L452R')
     * @returns {boolean}  True iff the mutation is NOT a stop mutation and is NOT an NSP one
     */
    isSupportedMut(protein, mut) {
      return (!mut.includes('stop') && !protein.startsWith('NSP'))
    }
  }
}
</script>

<style>
#app .inline-img .v-image {
  display: inline-block !important;
}
</style>