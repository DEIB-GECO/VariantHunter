<template>
  <div>
    <v-container fluid grid-list-xl style="justify-content: center; text-align: center; z-index: 1">
        <v-row justify="center" align="center" style="z-index: 1;">
                <div :id="timeName + '1'" style="width: 100%; height: 700px; user-select: none;
                -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
                 background-color: white; z-index: 1">
                </div>
        </v-row>
    </v-container>

<!--    <v-container fluid grid-list-xl style="justify-content: center; text-align: center; z-index: 1">-->
<!--        <v-row justify="center" align="center" style="z-index: 1">-->
<!--                <div :id="timeName + '2'" style="width: 100%; height: 500px; user-select: none;-->
<!--                -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;-->
<!--                 background-color: white; margin-top: 50px; z-index: 1">-->
<!--                </div>-->
<!--        </v-row>-->
<!--    </v-container>-->
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "BarChartPrevalence",
  props: {
    timeName: {required: true,},
    timeDistribution: {required: true},
    singleInfo: {required: true},
    sortColumn: {required: true,},
    descColumn: {required: true,},
    withLineages: {required: true}
  },
  data(){
    return {
      barChart: {
        title: {
        },
        grid: {
          top: 150,
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
              let icon0 = `<span data-tooltip="minimum" style="border-left: 2px solid #fff;display: inline-block;height: 10px;margin-right: 5px;width: 10px;">
                              <span style="background-color:${params.color}; border-radius: 100%; display: block;height: 10px;width: 10px;">
                              </span>
                            </span>`;
              let lineage =  `<span style="text-align: center; padding: 0; margin: 0;"><b>${params.seriesName} // ${params.name}</b></span>`

              let form ;
              if(params.seriesType === 'bar'){
                form = `<span><b>percentage:</b> ${Number(params.data['value']).toPrecision(3)}</span> <br />
                        <span><b># sequences:</b> ${params.data['total']}</span><br />`
              }
              else{
                form = `<span><b># sequences:</b> ${params.data}</span><br />`
              }

              return `${icon0} ${lineage} <br /><br />
                      ${form}`;
            },
        },
        // legend: {
        //   data: [],
        //   top: '20px',
        //   selectedMode: false,
        //   itemGap: 50,
        // },
        series: [],
        xAxis: {
            type: 'category',
            data: [],
        },
        yAxis: [
          {
            type: 'value',
            name: '% mut',
            position: 'left',
            offset: 10,
            min: 0,
            max: 100,
            axisLine: {
              show: true,
              lineStyle: {
                color: 'black'
              }
            },
          },
          {
            type: 'value',
            name: 'Tot Seq',
            position: 'right',
            offset: 10,
            min: 0,
            axisLine: {
              show: true,
              lineStyle: {
                color: 'red'
              }
            },
            splitLine: {
              show: false,
            },
            splitNumber: 5,
          },
        ],
        dataZoom: [
            {
                type: 'inside',
            },
          ],
      },
      // barChart2: {
      //   title: {
      //   },
      //   tooltip: {
      //       trigger: 'item',
      //   },
      //   // legend: {
      //   //   data: [],
      //   //   top: '20px',
      //   //   selectedMode: false,
      //   //   itemGap: 50,
      //   // },
      //   series: [],
      //   xAxis: {
      //       type: 'category',
      //       data: [],
      //   },
      //   yAxis: {
      //       type: 'value'
      //   },
      //   dataZoom: [
      //       {
      //           type: 'inside',
      //       },
      //     ],
      // },
      my_chart: null,
      // my_chart_2: null,
    }
  },
  computed: {
    ...mapState([]),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    customSort(items, index, isDesc) {
        if(index !== null && index !== undefined && index.length > 0){
          let i = 0;
          let len = index.length - 1;
          let idx = index[i];
          let desc = isDesc[i];
          if(idx !== null && idx !== undefined) {
            items.sort((a, b) => {
              if (!idx.includes('p_value') && !idx.includes('polyfit')) {
                if (idx === 'mut') {
                  if (desc) {
                    let pos_a = a['muts'][0]['loc'];
                    let pos_b = b['muts'][0]['loc'];
                    if (pos_a !== pos_b || i >= len) {
                      return pos_b < pos_a ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  } else {
                    let pos_a = a['muts'][0]['loc'];
                    let pos_b = b['muts'][0]['loc'];
                    if (pos_a !== pos_b || i >= len) {
                      return pos_b > pos_a ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                }
                else if(idx.includes('perc')){
                  let date = idx.replace('perc_with_absolute_number','');
                  let realKey = 'perc_with_mut_this_week' + date;
                  if (desc) {
                    if(a[idx] === null || a[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if(b[idx] === null || b[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return -1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if (b[realKey] !== a[realKey] || i >= len) {
                      return Number(b[realKey]) < Number(a[realKey]) ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  } else {
                    if(a[idx] === null || a[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if(b[idx] === null || b[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return -1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if (b[realKey] !== a[realKey] || i >= len) {
                      return Number(b[realKey]) > Number(a[realKey]) ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                }
                else{
                  if (desc) {
                      if (b[idx] !== a[idx] || i >= len) {
                        return b[idx] < a[idx] ? -1 : 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    } else {
                      if (b[idx] !== a[idx] || i >= len) {
                        return b[idx] > a[idx] ? -1 : 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                }
              }
              else{
                if (desc) {
                  if(a[idx] === null || a[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if(b[idx] === null || b[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return -1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if (b[idx] !== a[idx] || i >= len) {
                    return Number(b[idx]) < Number(a[idx]) ? -1 : 1;
                  }
                  else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                } else {
                  if(a[idx] === null || a[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if(b[idx] === null || b[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return -1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if (b[idx] !== a[idx] || i >= len) {
                    return Number(b[idx]) > Number(a[idx]) ? -1 : 1;
                  }
                  else{
                    return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                  }
                }
              }
            });
          }
          return items;
        }
        else{
          return items;
        }
    },
    singleCustomSort(a, b, i, len, index, isDesc) {
      let idx = index[i];
      let desc = isDesc[i];
      if (!idx.includes('p_value') && !idx.includes('polyfit')) {
        if (idx === 'mut') {
          if (desc) {
            let pos_a = a['muts'][0]['loc'];
            let pos_b = b['muts'][0]['loc'];
            if (pos_a !== pos_b || i >= len) {
              return pos_b < pos_a ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          } else {
            let pos_a = a['muts'][0]['loc'];
            let pos_b = b['muts'][0]['loc'];
            if (pos_a !== pos_b || i >= len) {
              return pos_b > pos_a ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
        }
        else if(idx.includes('perc')){
          let date = idx.replace('perc_with_absolute_number','');
          let realKey = 'perc_with_mut_this_week' + date;
          if (desc) {
            if(a[idx] === null || a[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if(b[idx] === null || b[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return -1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if (b[realKey] !== a[realKey] || i >= len) {
              return Number(b[realKey]) < Number(a[realKey]) ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          } else {
            if(a[idx] === null || a[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if(b[idx] === null || b[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return -1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if (b[realKey] !== a[realKey] || i >= len) {
              return Number(b[realKey]) > Number(a[realKey]) ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
        }
        else{
          if (desc) {
              if (b[idx] !== a[idx] || i >= len) {
                return b[idx] < a[idx] ? -1 : 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            } else {
              if (b[idx] !== a[idx] || i >= len) {
                return b[idx] > a[idx] ? -1 : 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
        }
      }
      else{
        if (desc) {
          if(a[idx] === null || a[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if(b[idx] === null || b[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return -1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if (b[idx] !== a[idx] || i >= len) {
            return Number(b[idx]) < Number(a[idx]) ? -1 : 1;
          }
          else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
        } else {
          if(a[idx] === null || a[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if(b[idx] === null || b[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return -1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if (b[idx] !== a[idx] || i >= len) {
            return Number(b[idx]) > Number(a[idx]) ? -1 : 1;
          }
          else{
            return this.singleCustomSort(a, b, i+1, len, index, isDesc);
          }
        }
      }

    },
    renderGraph(met2){
      let arrX = [];

      this.barChart.xAxis.data = [];
      this.barChart.series = [];

      let met = JSON.parse(JSON.stringify(this.customSort(met2, this.sortColumn, this.descColumn)));

      let analysis_date = this.singleInfo['date'];
      let max = this.singleInfo['weekNum'];
      let i = 0;
      let days = 7;
      while (i < max){
        arrX.unshift(analysis_date);
        let this_date = new Date(analysis_date);
        let previous_date = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
        analysis_date = previous_date.toISOString().split('T')[0];
        i = i + 1;
      }

      this.barChart.xAxis.data = arrX;
      // this.barChart2.xAxis.data = arrX;

      let objNumSeqDate = {};
      for(let j=0; j<met.length; j++) {
        for (let k = 0; k < arrX.length; k++) {
          let key1 = 'count_with_mut_this_week_' + arrX[k];
          let key2 = 'count_without_mut_this_week_' + arrX[k];
          // eslint-disable-next-line no-prototype-builtins
          if (met[j].hasOwnProperty(key1)) {
            // eslint-disable-next-line no-prototype-builtins
            if (!objNumSeqDate.hasOwnProperty(arrX[k])) {
              objNumSeqDate[arrX[k]] = (met[j][key1] + met[j][key2]);
            }
          }
        }
      }

      for(let j=0; j<met.length; j++){
        let singleArrY = [];
        for(let k=0; k<arrX.length; k++){
          let key1 = 'count_with_mut_this_week_' + arrX[k];
          let key2 = 'count_without_mut_this_week_' + arrX[k];
          // let total_seq = objNumSeqDate[arrX[k]];
          // eslint-disable-next-line no-prototype-builtins
          if(met[j].hasOwnProperty(key1)){
            let value = (met[j][key1] / (met[j][key1] + met[j][key2])) * 100;
            let obj = {value: value, name: arrX[k], total: met[j][key1]}
            singleArrY.push(obj);
          }
          else{
            let obj = {value: 0, name: arrX[k], total: 0}
            singleArrY.push(obj);
          }
        }
        let name;
        if(this.withLineages) {
          name = met[j]['lineage'] + '_' + met[j]['protein'] + '_' + met[j]['mut'];
        }
        else{
          name = met[j]['protein'] + '_' + met[j]['mut'];
        }
        this.barChart.series.push({
              name: name,
              type: 'bar',
              label: {
                show: true,
                position: 'top',
                formatter: '{a}',
                rotate: -90,
                offset: [-60, 5]
              },
              data: singleArrY,
          });
          // this.barChart.legend.data.push(name);
      }

      let arrNumSeqDate = [];
      for(let kk=0; kk<arrX.length; kk++){
        arrNumSeqDate.push(objNumSeqDate[arrX[kk]]);
      }

      this.barChart.series.push({
          name: 'Tot Seq',
          type: 'line',
          data: arrNumSeqDate,
          color: 'red',
          yAxisIndex: 1,
      });

      // this.barChart2.series.push({
      //     name: 'Tot Seq',
      //     type: 'bar',
      //     data: arrNumSeqDate,
      // });

      if(this.my_chart === null) {
        this.my_chart = echarts.init(document.getElementById(this.timeName + '1'));
      }
      else{
        this.my_chart.dispose();
        this.my_chart = echarts.init(document.getElementById(this.timeName + '1'));
      }
      this.my_chart.setOption(this.barChart, true);

      // if(this.my_chart_2 === null) {
      //   this.my_chart_2 = echarts.init(document.getElementById(this.timeName + '2'));
      // }
      // else{
      //   this.my_chart_2.dispose();
      //   this.my_chart_2 = echarts.init(document.getElementById(this.timeName + '2'));
      // }
      // this.my_chart_2.setOption(this.barChart2, true);
    },
  },
  mounted() {
    if(this.timeDistribution.length > 0) {
      this.renderGraph(JSON.parse(JSON.stringify(this.timeDistribution)));
    }
  },
  watch:{
    sortColumn(){
      if(this.descColumn[0]) {
        this.renderGraph(JSON.parse(JSON.stringify(this.timeDistribution)));
      }
    },
    descColumn(){
      this.renderGraph(JSON.parse(JSON.stringify(this.timeDistribution)));
    },
    timeDistribution(){
      this.renderGraph(JSON.parse(JSON.stringify(this.timeDistribution)));
    }
  }
}
</script>

<style scoped>

</style>