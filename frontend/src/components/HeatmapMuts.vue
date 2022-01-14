<template>
<v-container fluid grid-list-xl style="justify-content: center; z-index: 1; width: 1500px">
        <v-row justify="center" align="center" style="z-index: 1; position: relative; margin-top: 50px">
          <div :id="nameHeatmap" style="width: 100%; height: 500px; user-select: none;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0; border-width: 0;
           background-color: white; z-index: 1">
          </div>
        </v-row>
    </v-container>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as echarts from "echarts";

export default {
  name: "HeatmapMuts",
  props: {
    nameHeatmap: {required: true,},
    mutsData: {required: true},
    singleInfo: {required: true},
    sortColumn: {required: true,},
    descColumn: {required: true,},
    withLineages: {required: true}
  },
  data() {
    return {
      x_axis: [],
      y_axis: [],
      data_inside_heatmap: [],

      heatmap: {
        tooltip: {
            trigger: 'item',
            formatter: function (params) {

              let form = `<span><b>percentage:</b> ${Number(params.data[2]).toPrecision(3)}</span> <br />
                        <span><b># sequences with mut:</b> ${params.data[3]}</span><br />
                        <span><b># sequences total:</b> ${params.data[4]}</span><br />`

              return `${form}`;
            },
        },
        grid: {
          top: 100,
        },
        xAxis: {
          type: 'category',
          data: this.x_axis,
          splitArea: {
            show: true
          },
          axisLabel: {
            interval: '0',
            rotate: '-90',
          }
        },
        yAxis: {
          type: 'category',
          data: this.y_axis,
          splitArea: {
            show: true
          },
          axisLabel: {
            interval: '0',
          }
        },
        visualMap: {
          min: 0,
          max: 1,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '0px',
          color: ['#f6efa6', '#d88273', '#bf444c']
        },
        series: [{
          name: 'Distribution',
          type: 'heatmap',
          data: this.data_inside_heatmap,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            formatter: function (params) {
            return `${Number.parseFloat(params.data[2]).toPrecision(3)}`;
          },
          },
        }]
      },
      my_chart: null,
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
      this.x_axis = [];
      this.y_axis = [];
      this.data_inside_heatmap = [];

      let met = JSON.parse(JSON.stringify(this.customSort(met2, this.sortColumn, this.descColumn))).reverse();
      // let met = this.mutsData;
      let analysis_date = this.singleInfo['date'];
      let max = this.singleInfo['weekNum'];
      let i = 0;
      let days = 7;
      while (i < max){
        this.x_axis.unshift(analysis_date);
        let this_date = new Date(analysis_date);
        let previous_date = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
        analysis_date = previous_date.toISOString().split('T')[0];
        i = i + 1;
      }

      for(let j=0; j<met.length; j++){
        let name;
        if(this.withLineages) {
          name = met[j]['lineage'] + '_' + met[j]['protein'] + '_' + met[j]['mut'];
        }
        else{
          name = met[j]['protein'] + '_' + met[j]['mut'];
        }
        this.y_axis.push(name);
        for(let k=0; k<this.x_axis.length; k++){
          let key;
          let key_with_mut;
          let key_without_mut;
          if(this.withLineages) {
            key = 'p_value_comparative_mut_' + this.x_axis[k];
            key_with_mut = 'count_with_mut_this_week_' + this.x_axis[k];
            key_without_mut = 'count_without_mut_this_week_' + this.x_axis[k];
          }
          else{
            key = 'perc_with_mut_this_week_' + this.x_axis[k];
            key_with_mut = 'count_with_mut_this_week_' + this.x_axis[k];
            key_without_mut = 'count_without_mut_this_week_' + this.x_axis[k];
          }
          let value;
          let numerator;
          let denominator;
          // eslint-disable-next-line no-prototype-builtins
          if(met[j].hasOwnProperty(key)) {
            value = met[j][key];
            numerator = met[j][key_with_mut];
            denominator = (met[j][key_with_mut] + met[j][key_without_mut]);
          }
          else{
            value = '-';
            numerator = '-';
            denominator = '-';
          }
          let single_cell = [k, j, value, numerator, denominator, value];
          this.data_inside_heatmap.push(single_cell);
        }
      }

      this.heatmap.xAxis.data = this.x_axis;
      this.heatmap.yAxis.data = this.y_axis;
      this.heatmap.series[0].data = this.data_inside_heatmap;

      let len_y = this.y_axis.length;
      if(this.my_chart === null) {
        let height = (len_y * 20 + 300);
        this.my_chart = echarts.init(document.getElementById(this.nameHeatmap), null, {height: height}); //, null, {height: height}
      }
      else{
        this.my_chart.dispose();
        let height = (len_y * 20 + 300);
        this.my_chart = echarts.init(document.getElementById(this.nameHeatmap), null, {height: height}); //, null, {height: height}
      }
      this.heatmap.grid.height =  (len_y * 20);
      let elem = document.getElementById(this.nameHeatmap);
      elem.style['height'] = (len_y * 20 + 400).toString()  + 'px';

      if(this.withLineages){
       this.heatmap.visualMap.min = 0;
       this.heatmap.visualMap.max = 1;
       this.heatmap.visualMap.color = ['#f6efa6', '#d88273', '#bf444c'];
      }
      else{
        this.heatmap.visualMap.min = 0;
        this.heatmap.visualMap.max = 100;
        this.heatmap.visualMap.color = ['#bf444c', '#d88273', '#f6efa6'];
      }

      this.my_chart.setOption(this.heatmap, true);
    },
  },
  mounted() {
    this.renderGraph(JSON.parse(JSON.stringify(this.mutsData)));
  },
  watch: {
    sortColumn(){
      if(this.descColumn[0]) {
        this.renderGraph(JSON.parse(JSON.stringify(this.mutsData)));
      }
    },
    descColumn(){
      this.renderGraph(JSON.parse(JSON.stringify(this.mutsData)));
    },
    mutsData(){
      this.renderGraph(JSON.parse(JSON.stringify(this.mutsData)));
    }
  }
}
</script>

<style scoped>

</style>