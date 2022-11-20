<template>
  <!-- Keyboard Shortcuts feature-->
  <v-dialog v-model="showSnackbar" hide-overlay persistent>
    <v-snackbar  absolute v-model="showSnackbar" :timeout="-1" color="success">
    <v-card v-if="shortcut!==undefined" color="transparent" flat>
      <div class="text-uppercase font-weight-black text-center">
        <div class="mb-2"><span v-html="shortcuts[shortcut].kbd[0]"/>
          <v-icon small>mdi-plus</v-icon>
          <span v-html="shortcuts[shortcut].kbd[1]"/></div>
        {{ shortcuts[shortcut].title }}
      </div>
    </v-card>
  </v-snackbar>
  </v-dialog>
</template>

<script>
import {mapMutations, mapState} from "vuex";
import {shortcuts} from "@/utils/keyboardService";

export default {
  name: "KeyboardShortcuts",
  props: {
    filteredAnalyses: {},
  },
  data() {
    return {
      showSnackbar: false,
      shortcut: undefined,
      timeout:undefined,
    }
  },
  computed: {
    ...mapState(['currentAnalysisId']),

    shortcuts() {
      return shortcuts
    }
  },
  methods: {
    ...mapMutations(['setCurrentAnalysis']),

    onShortcut(id) {
      console.log(id)
      this.shortcut = id
      this.showSnackbar = true
      clearTimeout(this.timeout)
      this.timeout= setTimeout(()=>this.showSnackbar=false,1500)
    },

    newAnalysis() {
      this.onShortcut(0)
      this.setCurrentAnalysis(null)
    },
    prevAnalysis() {
      if(this.filteredAnalyses.length===0) return
      this.onShortcut(1)

      if (this.currentAnalysisId === null) {
        // Select the first element if in new analysis
        this.setCurrentAnalysis(this.filteredAnalyses[0])

      } else {
        // Select prev otherwise (if first, then select the last one)
        const index = this.filteredAnalyses.indexOf(this.currentAnalysisId);
        if (index >= 1 && index < this.currentAnalysisId.length)
          this.setCurrentAnalysis(this.filteredAnalyses[index - 1])
        else
          this.setCurrentAnalysis(this.filteredAnalyses.at(-1))

      }
    },
    nextAnalysis() {
      if(this.filteredAnalyses.length===0) return
      this.onShortcut(2)

      if (this.currentAnalysisId === null) {
        // Select the first element if in new analysis
        this.setCurrentAnalysis(this.filteredAnalyses[0])

      } else {
        // Select next otherwise (if last, then select the first one)
        const index = this.filteredAnalyses.indexOf(this.currentAnalysisId);
        if (index >= 0 && index < this.currentAnalysisId.length -1)
          this.setCurrentAnalysis(this.filteredAnalyses[index + 1])
        else
          this.setCurrentAnalysis(this.filteredAnalyses.at(0))

      }
    }
  },
  mounted() {
    window.onkeydown = (e) => {
      if (e.ctrlKey) {
        switch (e.key) {
          case 'n':
            this.newAnalysis()
            break;
          case 'ArrowUp':
            this.prevAnalysis()
            break;
          case 'ArrowDown':
            this.nextAnalysis()
            break;
        }
      }
    }
  }
}
</script>

<style scoped>

</style>