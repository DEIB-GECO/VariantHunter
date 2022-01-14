<template>
  <div>
    <v-btn @click="startAnalyseSelectedMutations()" color="primary" :disabled="selectedMuts.length === 0">
      ANALYSE SELECTED MUTATIONS ({{this.selectedMuts.length}})
    </v-btn>


  <v-dialog
      persistent
      v-model="dialogSelectedMuts"
      width="1600"
      >
        <v-card>
          <v-card-title class="white--text" v-bind:style="{ backgroundColor: 'grey' }">
            ANALYSE SELECTED MUTATIONS
            <v-spacer></v-spacer>
            <v-btn
                style="background-color: red"
                slot="activator"
                icon
                small
                color="white"
                @click="closeDialogSelectedMuts()"
            >
              X
            </v-btn>
          </v-card-title>

          <v-card-text class="text-xs-center">
            <v-layout row wrap justify-center style="padding-top: 30px; width: 100%">
              <v-flex class="no-horizontal-padding xs12 md4 lg4 d-flex" style="justify-content: center;">
                  <v-btn :disabled="checkPreviousDate" color="primary"
                         @click="analyzePeriod('previous')" style="z-index: 2; top:40px">
                     PREVIOUS PERIOD ({{weekNum}} WEEKS)
                  </v-btn>
              </v-flex>

              <v-flex class="no-horizontal-padding xs12 md4 lg4 d-flex" style="justify-content: center;">
              </v-flex>

              <v-flex class="no-horizontal-padding xs12 md4 lg4 d-flex" style="justify-content: center;">
                  <v-btn :disabled="checkNextDate" color="primary"
                         @click="analyzePeriod('next')" style="z-index: 2; top:40px">
                    NEXT PERIOD ({{weekNum}} WEEKS)
                  </v-btn>
              </v-flex>


              <v-flex class="no-horizontal-padding xs12 md12 lg12 d-flex" style="justify-content: center;">
                <BarChartPrevalence
                  time-name="timeChartSelectedMuts"
                  :time-distribution="mutsToPassToGraph"
                  :singleInfo = "singleInfoToSend"
                  :sortColumn="emptyArray"
                  :descColumn="emptyArray"
                  :withLineages="false"
                  style="padding: 0; width: 100%">
                </BarChartPrevalence>
              </v-flex>

              <v-flex class="no-horizontal-padding xs12 md12 lg12 d-flex" style="justify-content: center; margin-bottom: 50px">
                <v-btn color="primary" @click="downloadTableAnalyzedPeriods()">
                  DOWNLOAD TABLE ANALYZED PERIODS ({{minDate}} // {{maxDate}})
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card-text>

          <v-overlay :value="overlay" :absolute="true">
            <v-progress-circular
              indeterminate
              size="64"
            ></v-progress-circular>
          </v-overlay>

        </v-card>
      </v-dialog>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import BarChartPrevalence from "@/components/BarChartPrevalence";
import axios from "axios";

export default {
  name: "DialogAnalyseSelectedMuts",
  components: {BarChartPrevalence},
  props: {
    selectedMuts: {required: true,},
    singleInfo: {required: true,},
  },
  data() {
    return {
      dialogSelectedMuts: false,
      analysisDate: null,
      weekNum: null,
      granularity: null,
      location: null,
      checkNextDate: false,
      checkPreviousDate: false,
      listOfMutation: [],
      overlay: false,
      originalMuts: [],
      mutsToPassToGraph: [],
      singleInfoToSend: {},
      listOfPeriods: {},

      emptyArray: [],

      maxDate: null,
      minDate: null,
      totalNumOfWeek: null,
    }
  },
  computed: {
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    startAnalyseSelectedMutations() {
      this.listOfPeriods = {};
      this.prepareData();
      this.dialogSelectedMuts = true;
    },
    closeDialogSelectedMuts(){
      this.dialogSelectedMuts = false;
    },
    checkNextAndPreviousDate(){
      let analysisDate = new Date(this.analysisDate);
      let days = 7 * this.weekNum;
      let nextAnalysisDate = new Date(analysisDate.getTime() + (days * 24 * 60 * 60 * 1000));
      let previousAnalysisDate = new Date(analysisDate.getTime() - (days * 24 * 60 * 60 * 1000));
      let todayDate = new Date();
      let todayDateAfter4Week = new Date(todayDate.getTime() + (days * 24 * 60 * 60 * 1000));
      let startDate = new Date('2019-12-01');
      this.checkNextDate = nextAnalysisDate > todayDateAfter4Week;
      this.checkPreviousDate = previousAnalysisDate < startDate;
    },
    analyzePeriod(period){
      let this_date = new Date(this.analysisDate);
      let days = 7 * this.weekNum;
      if (period === 'next') {
        let dateToAnalyze = new Date(this_date.getTime() + (days * 24 * 60 * 60 * 1000));
        this.analysisDate = dateToAnalyze.toISOString().split('T')[0];
      } else if (period === 'previous') {
        let dateToAnalyze = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
        this.analysisDate = dateToAnalyze.toISOString().split('T')[0];
      }
      // eslint-disable-next-line no-prototype-builtins
      if(this.listOfPeriods.hasOwnProperty(this.analysisDate)){
        this.singleInfoToSend['date'] = this.analysisDate;
        this.mutsToPassToGraph = this.listOfPeriods[this.analysisDate];
      }
      else {
        this.overlay = true;
        let url = `/analyse_mutations_without_lineages/analyzePeriodSelectedMuts`;
        let to_send = {
          'granularity': this.granularity,
          'location': this.location,
          'date': this.analysisDate,
          'numWeek': this.weekNum,
          'listOfMutations': this.listOfMutation
        };

        axios.post(url, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.listOfPeriods[this.analysisDate] = JSON.parse(JSON.stringify(res));
              this.singleInfoToSend['date'] = this.analysisDate;
              this.mutsToPassToGraph = res;
              this.overlay = false;
            });
      }
      this.checkNextAndPreviousDate();
      this.calculateMinMaxDate();
    },
    prepareData(){
      this.overlay = false;
      this.singleInfoToSend = JSON.parse(JSON.stringify(this.singleInfo));
      this.originalMuts = JSON.parse(JSON.stringify(this.selectedMuts));
      let delayInMilliseconds = 50;
      let that = this;
      setTimeout(function() {
        that.mutsToPassToGraph = JSON.parse(JSON.stringify(that.selectedMuts));
      }, delayInMilliseconds);
      this.analysisDate = this.singleInfo['date'];
      this.weekNum = this.singleInfo['weekNum'];
      this.granularity = this.singleInfo['granularity'];
      this.location = this.singleInfo['location'];
      this.listOfMutation = [];
      this.listOfPeriods[this.analysisDate] = JSON.parse(JSON.stringify(that.selectedMuts));
      for(let j=0; j<this.selectedMuts.length; j++) {
        let singleMut = this.selectedMuts[j]['protein'] + '_' + this.selectedMuts[j]['mut'];
        this.listOfMutation.push(singleMut);
      }
      this.maxDate = null;
      this.minDate = null;
      this.totalNumOfWeek = this.weekNum;
      this.calculateMinMaxDate();
      this.checkNextAndPreviousDate();
    },
    calculateMinMaxDate(){
      if(this.maxDate === null){
        this.maxDate = this.analysisDate;
      }
      if(this.minDate === null){
        let this_date = new Date(this.analysisDate);
        let days = 7 * (this.weekNum - 1);
        let dateToAnalyze = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
        this.minDate = dateToAnalyze.toISOString().split('T')[0];
      }
      let dateMaxDate = new Date(this.maxDate);
      let dateMinDate = new Date(this.minDate);
      let dateAnalysisDate = new Date(this.analysisDate);
      if(dateAnalysisDate > dateMaxDate){
        this.totalNumOfWeek = this.totalNumOfWeek + this.weekNum;
        this.maxDate = this.analysisDate;
      }
      if(dateAnalysisDate <= dateMinDate){
        this.totalNumOfWeek = this.totalNumOfWeek + this.weekNum;
        let this_date = new Date(this.analysisDate);
        let days = 7 * (this.weekNum - 1);
        let dateToAnalyze = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
        this.minDate = dateToAnalyze.toISOString().split('T')[0];
      }
    },
    downloadTableAnalyzedPeriods(){
      let result_sorted = this.unionOfAllData();
      let headers = this.calculateHeaders();
      let text = this.json2csv(result_sorted, headers);
      let filename = 'mutsDiffusionTable_' + this.singleInfo['location'] + '_' + this.minDate + '_' + this.maxDate + '.csv';
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    json2csv(input, selected_headers) {
        var json = input;
        var fields = [];
        var fields2 = [];
        selected_headers.forEach(function (el) {
            fields.push(el.text.replaceAll("\n", ""));
        });
        selected_headers.forEach(function (el) {
            fields2.push(el.value.replaceAll("\n", ""));
        });
        var csv = json.map(function (row) {
            return fields2.map(function (fieldName) {
                let string_val;
                string_val = String(row[fieldName]);
                if(string_val === 'NaN'){
                  string_val = '0';
                }
                string_val = string_val.replaceAll("\n", " ");
                return JSON.stringify(string_val);
            }).join(',')
        });
        csv.unshift(fields.join(','));
        return csv.join('\r\n')
    },
    unionOfAllData(){
        let jsonResults = {};

        let totalRes = {'mut': 'Total', 'location': 'Total', 'protein': 'Total'};

        Object.keys(this.listOfPeriods).forEach(key => {
          for (let i = 0; i < this.listOfPeriods[key].length; i++){
            let analysis_date = key;
            for(let j=0; j<this.weekNum; j=j+1) {
              let mut = this.listOfPeriods[key][i]['mut'];
              let protein = this.listOfPeriods[key][i]['protein'];
              let location = this.listOfPeriods[key][i]['location'];
              let key1 = 'count_with_mut_this_week_' + analysis_date;
              let key2 = 'count_without_mut_this_week_' + analysis_date;
              let percentage = this.listOfPeriods[key][i][key1] / (this.listOfPeriods[key][i][key1] + this.listOfPeriods[key][i][key2]);

              // eslint-disable-next-line no-prototype-builtins
              if (totalRes.hasOwnProperty(analysis_date)) {
                if(totalRes[analysis_date] < (this.listOfPeriods[key][i][key1] + this.listOfPeriods[key][i][key2])){
                  totalRes[analysis_date] = (this.listOfPeriods[key][i][key1] + this.listOfPeriods[key][i][key2]);
                }
              }
              else{
                totalRes[analysis_date] = (this.listOfPeriods[key][i][key1] + this.listOfPeriods[key][i][key2]);
              }

              let jsonKey = location + '_' + protein + '_' + mut

              // eslint-disable-next-line no-prototype-builtins
              if (jsonResults.hasOwnProperty(jsonKey)) {
                jsonResults[jsonKey][analysis_date] = percentage;
              } else {
                jsonResults[jsonKey] = {'mut': mut, 'location': location, 'protein': protein};
                jsonResults[jsonKey][analysis_date] = percentage;
              }

              let this_date = new Date(analysis_date);
              let days = 7 ;
              let previous_date = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
              analysis_date = previous_date.toISOString().split('T')[0];
            }
          }
        });

        let arrayResults = [];

        Object.keys(jsonResults).forEach(key => {
          arrayResults.push(jsonResults[key]);
        });

        arrayResults.push(totalRes);

        return arrayResults;
    },
    calculateHeaders(){
      let predefined_headers = [
        {text: 'Location', value: 'location'},
        {text: 'Protein', value: 'protein'},
        {text: 'Mut', value: 'mut'},
      ]

      let additional_headers = [];
      let analysis_date = this.maxDate;
      for(let j=0; j<this.totalNumOfWeek; j=j+1){
        let single_header = {text: analysis_date, value: analysis_date};
        additional_headers.unshift(single_header);
        let this_date = new Date(analysis_date);
        let days = 7 ;
        let previous_date = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
        analysis_date = previous_date.toISOString().split('T')[0]
      }

      predefined_headers = predefined_headers.concat(additional_headers);
      return predefined_headers
    }
  },
  mounted() {
    this.prepareData();
  },
  watch: {

  }
}
</script>

<style scoped>

</style>