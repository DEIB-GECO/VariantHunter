<!--

  Component:    RowOptions
  Description:  Options to expand table rows and to show mutation history

  Props:
  ├── item:         Full table row data
  ├── isExpanded:   Boolean expanded flag for the row
  ├── expand:       Method to expand a row
  └── expandable:   Boolean flag set to true if the row can be expanded

-->

<template>
  <div>
    <!-- Expand option -->
    <v-tooltip bottom nudge-bottom="-3" allow-overflow z-index="10" max-width="400px" v-if="expandable" close-delay="0">
      <template v-slot:activator="{ on }">
        <v-btn icon small @click="expand(!isExpanded)" v-on="on" v-bind:id="idx+'-expand'">
          <v-icon>{{ isExpanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>
      </template>
      Show lineage breakdown for this mutation
    </v-tooltip>

    <!-- Mutation history option -->
    <v-tooltip bottom nudge-bottom="-3" allow-overflow z-index="10" max-width="400px" close-delay="0">
      <template v-slot:activator="{ on }">
        <v-btn icon small @click="showMutationHistory=true" v-on="on">
          <v-icon>mdi-information-variant</v-icon>
        </v-btn>
      </template>
      Show mutation history
    </v-tooltip>

    <!-- MUTATION HISTORY DIALOG --------------------------------------->
    <v-dialog v-if="showMutationHistory" v-model="showMutationHistory" max-width="850"
              transition="dialog-bottom-transition">
      <v-card>
        <!-- Dialog title -->
        <v-toolbar color="f_primary" class="dialog-title" dark flat>
          <v-icon left large>mdi-information-variant</v-icon>
          <span class="font-weight-regular">Information about</span> &nbsp;{{ item.protein + "_" + item.mut }}
          <v-spacer/>
          <icon-with-tooltip hover-color="error" bottom tip="Close" icon="mdi-close"
                             :click-handler="()=>showMutationHistory=false"/>
        </v-toolbar>

        <!-- Dialog content -->
        <v-container>
          <v-expand-transition>
            <!-- Actual mutation data -->
            <v-card-text v-if="!isLoadingDetails && !error" class="text-s-center dialog-text text-center">

              <!-- Characterized lineages -->
              <div class="pt-4 pb-7">
                <div class="text-h6 text-uppercase font-weight-bold">Characterized <span class="font-weight-black">Lineages</span>
                  <icon-with-tooltip icon="mdi-help-circle-outline" bottom tip="The characterizing mutations are identified as those that are
                        present in at least 50% of the lineage sequences." size="medium"/>
                </div>
                <div class="px-4">
                  <!-- Actual list of lineages names -->
                  <div class="py-2" v-if="characterizedLineages.length>0">
                    {{ item.protein + "_" + item.mut }} is a <span class="char-mut">characterizing mutation</span>
                    for the following lineages
                  </div>
                  <div class="py-2" v-else>No lineage is characterized by {{ item.protein + "_" + item.mut }}
                  </div>
                  <v-chip :color="getLineageColor(lineage).color" :light="!getLineageColor(lineage).isDark" small
                          :dark="getLineageColor(lineage).isDark" v-for="lineage in characterizedLineages"
                          :key="lineage" class="mr-1 mb-1">{{ lineage }}
                  </v-chip>
                </div>
              </div>
              <hr/>

              <!-- Decomposition over lineages -->
              <div class="pt-7">
                <div class="text-h6 text-uppercase font-weight-bold">Lineages <span
                    class="font-weight-black">breakdown</span></div>
                <div class="px-4">
                  <div class="py-2">
                    Sequences containing {{ item.protein + "_" + item.mut }} have the following distribution over
                    lineages <br/>(considering the entire dataset)
                  </div>
                  <!-- Table of decomposition -->
                  <v-simple-table dense>
                    <template v-slot:default>
                      <thead>
                      <tr>
                        <th class="text-center">Lineage</th>
                        <th class="text-center">Percentage</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr v-for="[lineage,{percentage, abs}] in Object.entries(mutationHistory)" :key="lineage">
                        <td :class="characterizedLineages.includes(lineage)?'char-mut':''">{{ lineage }}</td>
                        <td v-if="percentage>=0.5">{{ percentage.toPrecision(3) }}% ({{ abs }})</td>
                        <td v-else> &lt;0.5% ({{ abs }})</td>
                      </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </div>
              </div>

            </v-card-text>

            <!-- Error/loading -->
            <v-card-text v-else class="text-center py-5">
              <loading-sticker :standalone="true" :is-loading="error===undefined" :error="error" no-overlay
                               :loading-messages="[{text:'Analyzing mutation data',time:3000},{text:'This may take some time',time:6000},{text:'This may take up to 1 minute',time:15000},{text:'Almost done! Hang in there',time:30000}]"/>
            </v-card-text>
          </v-expand-transition>
        </v-container>

      </v-card>
    </v-dialog>

  </div>
</template>

<script>
import {getRandomColor} from "@/utils/colorService";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import IconWithTooltip from "../../general/basic/IconWithTooltip";

export default {
  name: "RowOptions",
  components: {IconWithTooltip, LoadingSticker},

  props: {
    /** Full table row data */
    item: {},

    /** Boolean expanded flag for the row */
    isExpanded: {},

    /** Method to expand a row */
    expand: {},

    /** Boolean flag set to true if the row can be expanded */
    expandable: {},

    /** Row number in the table */
    idx: {},
  },

  data() {
    return {
      /** Boolean visibility flag for the mutation history dialog */
      showMutationHistory: false,

      /** List of characterized lineages. Names only */
      characterizedLineages: [],
      /** Mutation history data.
       *  Hashmap in which: keys are names of lineages in which the mutation was found;
       *  values are objects of the form {abs, percentage} representing the number of
       *  sequences in absolute value and percentage.
       *  Example: {'BA.2':{'abs':12, 'percentage':53.4},...}
       */
      mutationHistory: {},

      /** Object storing lineage colors*/
      lineageColors: {},

      /** Boolean loading flag for the table and expansion */
      isLoadingDetails: false,
      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,
    }
  },

  watch: {
    /** On mutation history show, fetch history data */
    showMutationHistory(newVal) {
      if (newVal && this.characterizedLineages.length < 1 && Object.keys(this.mutationHistory).length < 1)
        this.fetchHistory()
    },

    /** When item changes (because of analysis change for example) clear data */
    item() {
      this.mutationHistory = {}
      this.characterizedLineages = []
      this.showMutationHistory = false
    }
  },

  methods: {
    /** Fetch mutation data from the server */
    fetchHistory() {
      this.error = undefined
      this.isLoadingDetails = true
      const url = `/explorer/getMutationHistory`
      const queryParams = {
        protein: this.item.protein,
        mut: this.item.mut,
      }

      this.$axios
          .get(url, {params: queryParams})
          .then(({data}) => {
            this.characterizedLineages = data['characterized_lineages']
            this.mutationHistory = data['history']
          })
          .catch((e) => this.error = e)
          .finally(() => this.isLoadingDetails = false)
    },

    /** Get a random color to be associated with the lineage */
    getLineageColor(lineage) {
      if (!this.lineageColors[lineage])
        this.lineageColors[lineage] = getRandomColor()
      return this.lineageColors[lineage]
    }
  },
}
</script>

<style scoped>

</style>