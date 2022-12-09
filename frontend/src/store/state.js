/**
 *  VUEX STATE
 *  State variables for the vuex state
 */

import {version} from '../../package.json'

export const state = {

    /**
     * Object defining the performed analysis. Each obj has the following structure
     *  id: unique integer identifier (ex: 0)
     *  starred: boolean star status flag
     *  query: {
     *      datasetInfo:{
     *          'file_type': metadata provider. Either 'gisaid' or 'nextstrain'
     *          'begin_date': 'beginning' or date (YYYY-mm-dd) defining lower bound on dataset
     *          'end_date': 'end' or date (YYYY-mm-dd) defining upper bound on dataset
     *          'filtered_countries' either 'all' or string of comma separated countries filtered
     *          'last_update': last update date of the dataset (last sequence date)
     *          'parsed_on': date of metadata parsing
     *          'version': backend app version used for the parsing
     *      }
     *      granularity: granularity level (ex: 'continent','country','region').
     *      location: {
     *          continent:  { id:     continent identifier, text:   continent name }
     *          country:    { id:     country identifier, text:   country name }
     *                      or null value if granularity==='continent'
     *          region:     { id:     region identifier, text:   region name }
     *                      or null value if granularity!=='region'
     *      }
     *      endDate: string reporting last day to be considered (ex: "2021-05-15")
     *      lineage: selected lineage for the analysis (ex. 'A.2.5.1'). Null value if N/A
     *      weeks: obj reporting the interested weeks in the following format YYYY/MM/DD - YYYY/MM/DD
     *             {w1:'...',w2:'...', w3:'...', w4:'2021/05/09 - 2021/05/15'}
     *      performedOn: full date of execution date (ex. 'Wed Dec 07 2022, 10:04')
     *  },
     *  tag: 'tagName'
     *  notes: 'string containing the notes' or null value if none
     *  characterizingMuts: ['protein_mut',...] or null if lineage independent
     *  muts: [{
     *     item_key: identifier of the row (ex: 'Spike_T12I')
     *     protein: protein value (ex: 'Spike')
     *     mut: mut value (ex: 'T12I')
     *     slope: slope value (ex: -0.248321375954962)
     *     f1, f2, f3, f4: frequency values for the weeks (ex: 1.6709439857174737)
     *     w1, w2, w3, w4: number of sequences for the weeks (ex: 599)
     *     p_value_with_mut: p-value associated with the slope (ex: 1.6478444582562806e-25)
     *     p_value_without_mut: p-value associated with the slope (ex: 0.8666225744922994)
     *     p_value_comp: p-value associated with the slope (ex: 3.7226377268156197e-26)
     *  }]
     *  totSeq:{
     *      w1,w2,w3,w4: overall number of sequences collected in the weeks
     *  }
     */
    analyses: {},

    /** Local options for the analysis. Each object has:
     *  {
     *      useLocalOpt: Boolean flag set to true if the scope for the analysis is local.
     *      protein: null, muts: [], rowKeys: [],               // local filtering options
     *      sortingIndexes:[ "slope" ], isDescSorting:[true]    // local ordering options
     *  }
     */
    localOpt: {},

    /** Tags applied to the analysis
     *  {
     *      'tagName':{
     *          tagColor: '#colorCode'
     *          protein: null, muts: [], rowKeys: [],               // custom filtering options
     *          sortingIndexes:[ "slope" ], isDescSorting:[true]    // custom ordering options
     *          createdAt: full date of the creation date (ex: 'Mon Dec 05 2022 18:11:14 GMT+0100')
     *      }
     *  }
     */
    tags: {},

    /** Identifier of the currently shown analysis or null value */
    currentAnalysisId: null,

    /** Selected location object including {id, text} */
    selectedLocation: null,
    /** Possible location objects including {id, text} */
    possibleLocations: [],
    /** Info about possible locations {'id'{'type', 'country': {'id', 'text'}, 'continent' {'id', 'text'}}} */
    possibleLocationsInfo: {},

    /** Selected analysis period as [start, end] */
    selectedDate: null,

    /** Selected lineage. It consists of {'items':['BA.4.1'], 'groups':{'BA.1.*: ['BA.1',...]}}, 'count'} */
    selectedLineage: {items: [], groups: [], count: 0},
    /** Possible lineages */
    possibleLineages: [],
    /** Info about possible lineages {'lineage': integer_count} */
    possibleLineagesInfo: {},

    /** Last update date of the dataset (last sequence date) */
    lastUpdate: null,
    /** Dataset info for the dataset in use
     *  {
     *      'fileType': metadata provider. Either 'gisaid' or 'nextstrain'
     *      'beginDate': 'beginning' or date (YYYY-mm-dd) defining lower bound on dataset
     *      'endDate': 'end' or date (YYYY-mm-dd) defining upper bound on dataset
     *      'filteredCountries' either 'all' or string of comma separated countries filtered
     *      'parsedOn': date of metadata parsing
     *  }
     */
    datasetInfo: {},

    /** Current step of the app-tour */
    tourStep: 'tour',

    /** Reset flag, if set to true the storage is cleared */
    reset: false,

    /** Global loading flag */
    loading: false,

    /** Frontend app version*/
    version: version,
}