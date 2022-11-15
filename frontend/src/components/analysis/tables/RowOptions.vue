<template>
  <div>
    <!-- Expand option -->
    <v-tooltip bottom nudge-bottom="-3" allow-overflow z-index="10" max-width="400px" v-if="expandable">
      <template v-slot:activator="{ on }">
        <v-btn icon small @click="expand(!isExpanded)" v-on="on">
          <v-icon>{{ isExpanded ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>
      </template>
      Show lineage breakdown for this mutation
    </v-tooltip>

    <!-- Mutation history option -->
    <v-tooltip bottom nudge-bottom="-3" allow-overflow z-index="10" max-width="400px">
      <template v-slot:activator="{ on }">
        <v-btn icon small @click="showMutationHistory=true" v-on="on">
          <v-icon>mdi-information-variant</v-icon>
        </v-btn>
      </template>
      Show mutation history
    </v-tooltip>

    <!-- Dialog element-->
    <v-dialog v-model="showMutationHistory" max-width="850" transition="dialog-bottom-transition">
      <v-card>
        <!-- Dialog title -->
        <v-toolbar color="f_primary" class="dialog-title" dark flat>
          <v-icon left large>mdi-information-variant</v-icon>
          <span class="font-weight-regular">Information about</span> &nbsp;{{ item.protein + "_" + item.mut }}
        </v-toolbar>

        <!-- Dialog content -->
        <v-container>
          <v-expand-transition>
            <v-card-text v-if="!isLoadingDetails && !error" class="text-s-center dialog-text text-center">
              <div class="pt-4 pb-7">
                <div class="text-h6 text-uppercase font-weight-bold">Characterized <span class="font-weight-black">Lineages</span></div>
                <div class="px-4">
                  <div class="py-2" v-if="characterizedLineages.length>0">
                    {{ item.protein + "_" + item.mut }} is a <span class="char-mut">characterizing mutation</span> for
                    the following lineages
                  </div>
                  <div class="py-2" v-else>No lineage is characterized by {{ item.protein + "_" + item.mut }}
                  </div>
                  <v-chip :color="getLineageColor().color" :light="!getLineageColor().isDark" :dark="getLineageColor().isDark" v-for="lineage in characterizedLineages"
                          :key="lineage" class="mr-1 mb-1">{{ lineage }}
                  </v-chip>
                </div>
              </div>
              <hr/>
              <div class="pt-7">
                <div class="text-h6 text-uppercase font-weight-bold">Lineages <span class="font-weight-black">breakdown</span></div>
                <div class="px-4">
                  <div class="py-2">
                    Sequences containing {{ item.protein + "_" + item.mut }} have the following distribution over
                    lineages <br/>(considering the entire dataset)
                  </div>
                  <v-simple-table>
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
            <v-card-text v-else-if="error" class="text-s-center dialog-text error--text py-5 text-center">
              <span class="font-weight-black">An error occurred. </span> Try again later.
            </v-card-text>
            <v-card-text v-else class="text-center py-5">
              <loading-sticker :standalone="true" :is-loading="true"
                             :loading-messages="[{text:'Analyzing mutation data',time:3000},{text:'This may take some time',time:6000},{text:'This may take up to 1 minute',time:15000},{text:'Almost done! Hang in there',time:30000}]"/>
            </v-card-text>
          </v-expand-transition>
        </v-container>

        <!-- Dialog actions -->
        <v-card-actions class="justify-end">
          <v-btn text @click="showMutationHistory = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import {mapState} from "vuex";
import axios from "axios";
import {getRandomColor} from "@/utils/colorService";
import LoadingSticker from "@/components/general/basic/LoadingSticker";

export default {
  name: "RowOptions",
  components: {LoadingSticker},
  props: {
    /** Row item */
    item: {},

    /** Row expanded flag */
    isExpanded: {},

    /** Row expand function */
    expand: {},

    /** Show expand function flag */
    expandable:{},
  },
  data() {
    return {
      showMutationHistory: false,

      characterizedLineages: [],
      mutationHistory: {},

      error: undefined,
      isLoadingDetails: false,
    }
  },
  watch: {
    showMutationHistory(newVal) {
      if (newVal && this.characterizedLineages.length < 1 && Object.keys(this.mutationHistory).length < 1)
        this.fetchHistory()
    },
    item() {
      this.mutationHistory = {}
      this.characterizedLineages = []
      this.showMutationHistory = false
    }
  },
  methods: {
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
          .catch((e) => {
            this.error = e
          })
          .finally(() => {
            this.isLoadingDetails = false
          })
    },

    getLineageColor(){
      return getRandomColor()
    }
  }
}
</script>

<style scoped>

</style>