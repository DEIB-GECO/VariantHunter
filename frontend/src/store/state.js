/**
 *  VUEX STATE
 *  State variables for the vuex state
 */

import {ex1,ex2} from "@/store/testData";

export const state = {

    /**
     * Analysis: object defining the performed analysis. Each obj has the following structure
     *  id: unique identifier (ex: 0)
     *  starred: star status flag
     *  query: {
     *      granularity: granularity level (ex: 'continent','country','region').
     *      location: {
     *          continent: selected continent for the analysis (ex: 'Europe')
     *          country: selected country for the analysis (ex: 'Italy'). Null value if N/A
     *          region: selected region for the analysis (ex: 'Italy'). Null value if N/A
     *      }
     *      endDate: string reporting last day to be considered (ex: "2021-05-15")
     *      lineage: selected lineage for the analysis (ex. 'A.2.5.1'). Null value if N/A
     *      weeks: obj reporting the interested weeks in the following format YYYY/MM/DD - YYYY/MM/DD
     *             {w1:'...',w2:'...', w3:'...', w4:'2021/05/09 - 2021/05/15'}
     *  },
     *  useGlobalFilters: true iff global filters must be used instead of local ones
     *  filteringOpt: {
     *      protein: string representing the filtered protein or null
     *      muts: array [] of filtered mutations
     *      rowKeys: array [] of selected row keys
     *      sortingIndexes: array []  of sorting columns
     *      isDescSorting: array [] of boolean representing the sorting directions
     *  }
     *  characterizingMuts: ['protein_mut',...] or null if lineage independent
     *  muts: [{
     *     protein: protein value (ex: 'Spike')
     *     mut: mut value (ex: 'T12I')
     *     slope: slope value (ex: -0.248321375954962)
     *     f1, f2, f3, f4: frequency values for the weeks (ex: 1.6709439857174737)
     *     w1, w2, w3, w4: number of sequences for the weeks (ex: 599)
     *     p_value_with_mut: pvalue associated with the slope (ex: 1.6478444582562806e-25)
     *     p_value_without_mut: pvalue associated with the slope (ex: 0.8666225744922994)
     *     p_value_comp: pvalue associated with the slope (ex: 3.7226377268156197e-26)
     *  }]
     *  totSeq:{
     *      w1,w2,w3,w4: overall number of sequences collected in the weeks
     *  }
     */
    analyses:{0:ex1, 1:ex2},
    localFilteringOpt: {0:{useGlobalFilters: true, protein: null, muts: [], rowKeys: []},1:{useGlobalFilters: true, protein: null, muts: [], rowKeys: []}},
    localOrderingOpt: {0:{sortingIndexes:[ "slope" ], isDescSorting:[true]}, 1:{sortingIndexes:[ "slope" ], isDescSorting:[true]}},


    /** currentAnalysisId: id of the currently shown analysis or null value */
    currentAnalysisId: null,
    globalFilteringOpt: {protein: null, muts: [], rowKeys: []},
    globalOrderingOpt: {sortingIndexes:[ "slope" ], isDescSorting:[true]},

    /** Selected location (continent, country or region based on granularity) */
    selectedLocation: null,
    possibleLocations: [],
    possibleLocationsInfo: {},

    /** Date: selected date */
    selectedDate: null,

    /** Lineage: selected lineage */
    selectedLineage: null,
    possibleLineages: [],

    /** lastUpdate: last update date */
    lastUpdate: null,

    reset: false,
    loading:false,
}