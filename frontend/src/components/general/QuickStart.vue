<!--

  Component:    QuickStart
  Description:  Section with featured examples

-->

<template>
  <v-row class="px-5 mt-8">
    <v-container>
      <!-- Intro text -->
      <v-row>
        <v-col>
          <div class="text-h5 font-weight-black primary--text pb-3" id="featured">
            Featured Analyses
          </div>

          <v-sheet class="mx-auto rounded-xl" color="transparent" flat min-width="100%" max-width="fit-content">
            <v-slide-group class="px-0" show-arrows>
              <v-slide-item v-for="(example,idx) in examples" :key="idx">
                <!-- Example card element -->
                <v-card class="mr-3 mt-0 pa-5 pb-2 rounded-xl text-left" flat max-width="50vw" width="340px"
                        color="primary">
                  <!-- Example title and intro -->
                  <div class="example-title text_var2--text" @click="show(idx)">
                    {{ example.title }}
                  </div>
                  <div class="example-intro text_var2--text pt-1 pb-3">
                    {{ example.intro }}
                  </div>

                  <div class="mb-2">
                    <v-chip x-small :color="locationColor(example.granularity)" dark
                            class="text-uppercase mr-1 mb-1">
                      {{ example.granularity }}
                    </v-chip>
                    <v-chip x-small :color="example.type==='ls'?'#1f2215':'#3398DC'" dark
                            class="text-uppercase mr-1 mb-1">
                      {{ example.type === 'ls' ? "lineage-specific" : "lineage-independent" }}
                    </v-chip>
                  </div>

                  <!-- Example actions -->
                  <v-btn class="mr-2 mb-2" rounded x-small elevation="0" @click="show(idx)">
                    <v-icon left x-small>mdi-plus</v-icon>
                    Details
                  </v-btn>
                  <v-btn class="mb-2" rounded x-small elevation="0" @click="open(idx)" :id="'featured-'+idx">
                    <v-icon left x-small>mdi-lead-pencil</v-icon>
                    Open
                  </v-btn>
                </v-card>
              </v-slide-item>
            </v-slide-group>

            <!-- EXAMPLE DIALOG  -->
            <v-dialog v-model="showDialog" max-width="900" transition="dialog-bottom-transition">
              <v-card class="rounded-xl">
                <!-- Dialog toolbar -->
                <v-toolbar class="dialog-title pl-2" color="transparent" flat>
                  <v-spacer></v-spacer>
                  <v-btn icon @click="showDialog=false">
                    <v-icon>mdi-close-thick</v-icon>
                  </v-btn>
                </v-toolbar>

                <v-card-text class='text-s-center dialog-text'>
                  <v-container>
                    <v-row justify="center" no-gutters>

                      <!-- Description -->
                      <v-col class="text-left" cols="9">
                        <div class="text-right">
                          <v-chip class="mt-0 mb-2 hidden-xs text-uppercase" color="f_tertiary" light x-small>
                            featured example
                          </v-chip>
                        </div>

                        <h3 class="font-weight-bold text-h5 primary--text">{{ examples[opened].title }}</h3>
                        <div class="my-2">
                          <v-chip x-small :color="locationColor(examples[opened].granularity)" dark
                                  class="text-uppercase mr-1 mb-1">
                            {{ examples[opened].granularity }}
                          </v-chip>
                          <v-chip x-small :color="examples[opened].type=='ls'?'#1f2215':'#3398DC'" dark
                                  class="text-uppercase mr-1 mb-1">
                            {{ examples[opened].type == 'ls' ? "lineage-specific" : "lineage-independent" }}
                          </v-chip>
                        </div>

                        <p v-html="examples[opened].body"/>

                        <v-btn class="my-3" color="f_tertiary" light elevation="0" rounded small @click="open(opened)">
                          <v-icon left small>mdi-lead-pencil</v-icon>
                          Open example in Variant Hunter
                        </v-btn>
                      </v-col>

                    </v-row>
                  </v-container>
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-sheet>
        </v-col>

        <link-to v-model="params" triggered/>

      </v-row>
    </v-container>
  </v-row>
</template>

<script>
import {examples} from "@/store/examples";
import {getLocationColor} from "@/utils/colorService";
import LinkTo from "@/components/views/LinkTo.vue";

export default {
  name: "QuickStart",
  components: {LinkTo},

  data() {
    return {
      /** Boolean flag set to true iff the example dialog is shown */
      showDialog: false,

      /** Identifier for the currently opened example */
      opened: 0,

      /** Params object when triggered manually */
      params: undefined,
    }
  },

  computed: {
    /** Examples */
    examples() {
      return examples
    }
  },

  methods: {
    /**
     * Show the dialog related to a given example idx
     * @param idx   Example index
     */
    show(idx) {
      this.showDialog = true
      this.opened = idx
    },

    /**
     * Run the example with a given example idx
     * @param idx   Example index
     */
    open(idx) {
      this.showDialog = false

      let url = this.examples[idx].url  // example URL
      const urlStart = url.indexOf('?')
      if (urlStart > -1) {
        url = url.slice(urlStart + 1) // cut not relevant part
        url = new URLSearchParams(url)

        // Set params to trigger search
        this.params = {
          type: url.get('type'),
          locationName: url.get('locationName'),
          date: url.get('date'),
          lineages: url.getAll('lineages')
        }
      }
    },

    /**
     * Mapping for getLocationColor
     */
    locationColor(granularity) {
      return getLocationColor(granularity)
    }
  }
}
</script>

<style scoped>
.example-title {
  font-weight: 700;
  font-size: 16px;
  line-height: 17px;
}

.example-intro {
  font-weight: 300;
  font-size: 14px;
  line-height: 14px;
}
</style>