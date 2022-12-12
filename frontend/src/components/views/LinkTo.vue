<!-- TODO -->
<template>
  <div>
    <v-container v-if="!triggered" class="mt-14 pt-14 text-center">
      <div class="text-h4 font-weight-bold">You are being redirected...</div>
      <div class="load-elem">
        <loading-sticker :is-loading="isLoading" :error="error" :standalone="true" no-overlay
                         :loading-messages="[{text:'You are being redirected',time:0},{text:'Analyzing sequence data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>
      </div>
      <div class="mt-14">
        <router-link :to="{ name: 'Home'}">
          <v-btn color='text_var1' class="text_var2--text" depressed rounded>
            <v-icon left>mdi-exit-run</v-icon>
            Go to the homepage
          </v-btn>
        </router-link>
      </div>

    </v-container>
    <loading-sticker v-else :is-loading="isLoading" :error="error"
                     :loading-messages="[{text:'You are being redirected',time:0},{text:'Analyzing sequence data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>

    <!-- No data alert -->
    <no-data-alert v-model="noDataWarning"/>
  </div>
</template>

<script>
import NoDataAlert from "@/components/general/NoDataAlert.vue";
import LoadingSticker from "@/components/general/basic/LoadingSticker.vue";
import {mapActions} from "vuex";

export default {
  name: "LinkTo",
  components: {LoadingSticker, NoDataAlert},

  props: {
    /** Params object when triggered manually */
    value: {},

    /** Boolean flag set to true if analysis is not performed automatically */
    triggered: Boolean,
  },

  data() {
    return {
      /** Boolean loading flag for the table and expansion */
      isLoading: false,
      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,

      /** Boolean visibility flag for the no data warning popup*/
      noDataWarning: false,
    }
  },

  computed: {
    /** Params object when triggered manually */
    params: {
      set(newVal) {
        this.$emit('input', newVal)
      },
      get() {
        return this.value
      }
    }
  },

  watch: {
    value(newVal, oldVal) {
      if (!oldVal && newVal)
        this.sendAnalysis(newVal)
    }
  },

  methods: {
    ...mapActions(['addAnalysis']),

    /**
     * Triggers the analysis request to the server
     */
    sendAnalysis({type, location, date, lineages}) {
      if (typeof lineages === "string")
        lineages = [lineages]
      else if (!lineages) {
        lineages = []
      }

      this.isLoading = true
      this.error = undefined
      const url = (type === 'li') ? "/lineage_independent/getStatistics" : "/lineage_specific/getStatistics"
      const queryParams = new URLSearchParams();
      queryParams.append('location', location)
      queryParams.append('date', date)

      // Add lineages data
      if (lineages.length > 0) {
        lineages.forEach(name => queryParams.append("lineages", name))
      }

      this.$axios
          .get(url, {params: queryParams}).then(({data}) => data)
          .then(({rows, tot_seq, characterizing_muts = null, metadata}) => {
            if (rows.length > 0) {
              // Save the search parameters and results
              this.addAnalysis({rows, tot_seq, characterizing_muts, metadata})
              if (!this.triggered) // redirect if not triggered
                this.$router.push({name: 'Home'})

            } else {
              this.noDataWarning = true
            }
            this.params = undefined // in any case reset params
          })
          .catch((e) => this.error = e)
          .finally(() => this.isLoading = false)
    },
  },

  mounted() {
    if (!this.triggered)
      this.sendAnalysis(this.$route.query)
  }
}
</script>

<style scoped>
.load-elem {
  margin: auto;
  max-width: 350px;
}
</style>