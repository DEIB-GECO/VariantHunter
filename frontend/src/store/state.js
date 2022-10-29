/**
 *  VUEX STATE
 *  State variables for the vuex state
 */

import {ex1,ex2} from "@/store/testData";

export const state = {

    /**
     * Analysis: array of objects defining the performed analysis. Each obj has the following structure
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
     *  }
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
    analyses:[ex1,ex2],

    /** currentAnalysis: currently shown analysis or null value */
    currentAnalysis: 0,

    /** Granularity: selected option */
    selectedGranularity: null,

    /** Selected continent */
    selectedContinent: null,

    /** Selected country */
    selectedCountry: null,

    /** Selected region */
    selectedRegion: null,

    /** Selected location (continent, country or region based on granularity) */
    selectedLocation: null,

    /** Date: selected date */
    selectedDate: null,

    /** Lineage: selected lineage */
    selectedLineage: null,

    primary_color: '#014878',
  secondary_color: '#35B1ECFF',
  tertiary_color_light: '#D2ECF8FF',
  tertiary_color_dark: '#1976D2FF',
}