<template>
  <v-container fluid grid-list-xl style="justify-content: center; padding: 0;">
    <v-tabs v-model="selectedTabAnalyze"
              :background-color="menu_color"
              dark
              show-arrows
              :slider-color="toolbar_color"
              slider-size="6"
              class="containTabs"
              height="60">


        <v-tab id="tab0" style="border-right: black solid 1px; width: 30%; border-bottom: solid black 1px">
           LINEAGE INDEPENDENT
        </v-tab>

        <v-tab id="tab1" style="border-right: black solid 1px; width: 30%; border-bottom: solid black 1px">
           LINEAGE SPECIFIC
        </v-tab>

        <v-tab-item class="lol">
          <MainPageWithoutLineages></MainPageWithoutLineages>
        </v-tab-item>

        <v-tab-item class="lol">
          <MainPageWithLineages></MainPageWithLineages>
        </v-tab-item>

      </v-tabs>

      <v-overlay :value="overlay">
        <v-progress-circular
          indeterminate
          size="64"
        ></v-progress-circular>
      </v-overlay>

  </v-container>
</template>


<script>
import axios from "axios";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import MainPageWithLineages from "@/components/MainPageWithLineages";
import MainPageWithoutLineages from "@/components/MainPageWithoutLineages";

export default {
  name: "MenuPage",
  components: {MainPageWithoutLineages, MainPageWithLineages},
  data() {
    return {
      selectedTabAnalyze: 0,
      overlay: true,
      finished_api: 0,
    }
  },
  computed: {
    ...mapState(['toolbar_color', 'menu_color', 'background_card_color']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations(['setAllGeo', 'setAllLineages']),
    ...mapActions([]),
  },
  watch:{
    finished_api(){
      if(this.finished_api === 2){
        this.overlay = false;
      }
    },
    selectedTabAnalyze(){
      let i = 0;
      while(i < 2){
        let id = 'tab' + i;
        if (i === this.selectedTabAnalyze){
          let elem = document.getElementById(id);
          //elem.style.fontSize = '15px';
          elem.style['font-weight'] = 'bold';
        }
        else{
          let elem = document.getElementById(id);
          //elem.style.fontSize = '12px';
          elem.style['font-weight'] = 'normal';
        }
        i = i + 1;
      }
    },
  },
  mounted() {
    let i = 0;
    while(i < 2){
      let id = 'tab' + i;
      if (i === this.selectedTabAnalyze){
        let elem = document.getElementById(id);
        //elem.style.fontSize = '15px';
        elem.style['font-weight'] = 'bold';
      }
      else{
        let elem = document.getElementById(id);
        //elem.style.fontSize = '12px';
        elem.style['font-weight'] = 'normal';
      }
      i = i + 1;
    }

    let url = `/analyse_mutations/getAllGeo`;
    axios.get(url)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.finished_api = this.finished_api + 1;
      this.setAllGeo(res);
    });

    let url2 = `/analyse_mutations/getAllLineage`;
    axios.get(url2)
    .then((res) => {
      return res.data;
    })
    .then((res) => {
      this.finished_api = this.finished_api + 1;
      this.setAllLineages(res);
    });
  }
}
</script>

<style scoped>

  .lol {
      height: 83.5vh;
      width: 100%;
      overflow-y:auto;
      float:left;
      position:relative;
  }

  .containTabs{
    width: 100%;
    float:left;
    position:relative;
  }

</style>