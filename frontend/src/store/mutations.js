/**
 *
 *  STORE MUTATIONS METHODS
 *
 *  Usage:        commit('mutationName',payload)
 *  Definition:   mutationName(state,payload){}
 *
 **/

import {computeDateLabel} from "@/store/utils/utils";
import Vue from "vue";

let nextAnalysisId = 2

export const mutations = {
    /**
     * Sets the current analysis id
     * @param state
     * @param id    Id to be set
     */
    setCurrentAnalysis(state, id) {
        console.log("setCurrentAnalysis to " + id)
        state.currentAnalysisId = id
    },

    /**
     * Add a filtering option
     * @param state
     * @param global    True iff the filtering option has global scope
     * @param opt       Filtering parameter to be set
     * @param value     Value to be filtered
     */
    setFilterOpt(state, {global = true, opt, value}) {
        console.log("setFilter of " + opt + " to " + value)

        if (global) {
            Vue.set(state.globalFilteringOpt,opt, value)
        } else {
            const id=state.currentAnalysisId
            Vue.set(state.localFilteringOpt[id],opt, value)
        }
    },

    /**
     * Add an ordering option
     * @param state
     * @param global    True iff the ordering option has global scope
     * @param opt       Ordering parameter to be set
     * @param value     Value to be ordering
     */
    setOrderOpt(state, {global = true, opt, value}) {
        console.log("setOrder of " + opt + " to " + value)
        if (global) {
            Vue.set(state.globalOrderingOpt,opt, value)
        } else {
            const id=state.currentAnalysisId
            Vue.set(state.localOrderingOpt[id],opt, value)
        }
    },

    /**
     * Sets the starred flag of an analysis
     * @param state
     * @param id        Analysis id
     * @param starred   Boolean value for the starred flag
     */
    setStarredAnalysis(state, {id, starred = true}) {
        console.log("setStarredAnalysis of " + id + " to " + starred)
        state.analyses[id].starred = starred
    },

    /**
     * Add a new analysis
     * @param state
     * @param rows                      Mutations rows
     * @param tot_seq                   Tot seq collected in the weeks
     * @param characterizing_muts       Characterizing mutations for the specific lineage
     * @param mode                      Mode of analysis. Either 'ls' or 'li'.
     */
    addAnalysis(state, {rows, tot_seq, characterizing_muts=null, mode}) {
        // Save current analysis data
        const locationInfo = state.possibleLocationsInfo[state.selectedLocation]
        const endDate = state.selectedDate[1]

        const assignedId = nextAnalysisId
        nextAnalysisId++

        Vue.set(state.analyses,assignedId, {
            id: assignedId,
            starred: false,
            query: {
                granularity: locationInfo.type,
                location: {
                    continent: locationInfo.type === 'continent' ? state.selectedLocation : locationInfo.continent,
                    country: locationInfo.type === 'country' ? state.selectedLocation : locationInfo.country,
                    region: locationInfo.type === 'region' ? state.selectedLocation : null,
                },
                endDate: endDate,
                lineage: mode === 'ls' ? state.selectedLineage : null,
                weeks: {
                    w1: computeDateLabel(endDate, 27, 21), w2: computeDateLabel(endDate, 20, 14),
                    w3: computeDateLabel(endDate, 13, 7), w4: computeDateLabel(endDate, 6, 0)
                }
            },
            characterizingMuts: characterizing_muts,
            rows: rows,
            totSeq: {
                w1: tot_seq[0], w2: tot_seq[1], w3: tot_seq[2], w4: tot_seq[3]
            }
        })

        // Preset filtering and ordering options
        Vue.set(state.localFilteringOpt,assignedId, {
            useGlobalFilters: true, protein: null, muts: [], rowKeys: []
        })
        Vue.set(state.localOrderingOpt,assignedId,  {
            sortingIndexes:[ "slope" ], isDescSorting:[true]
        })

        // Show the newly created analysis
        state.currentAnalysisId = assignedId
    },

    /**
     * Remove an analysis given its id
     * @param state
     * @param id        Analysis id
     */
    removeAnalysis(state, id) {
        console.log("removeAnalysis " + id)
        if (id === state.currentAnalysisId)
            state.currentAnalysisId = null

        Vue.delete(state.analyses,id)
        Vue.delete(state.localFilteringOpt,id)
        Vue.delete(state.localOrderingOpt,id)
    },


    setLocation(state, newValue) {
        console.log("setLocation " + newValue)
        state.selectedLocation = newValue
    },
    setLocations(state, newValue) {
        console.log("setLocations " + newValue)
        state.possibleLocations = newValue
    },
    setLocationsInfo(state, newValue) {
        console.log("setLocationsInfo " + newValue)
        state.possibleLocationsInfo = newValue
    },

    setLineage(state, newValue) {
        console.log("setLineage " + newValue)
        state.selectedLineage = newValue
    },
    setLineages(state, newValue) {
        console.log("setLineages " + newValue)
        state.possibleLineages = newValue
    },

    setDate(state, newValue) {
        console.log("setDate " + newValue)
        if (newValue !== null && newValue.length === 1) {
            // Date has been set from the picker (and has the form [endDate])
            const endDate = newValue[0]
            const startDate = new Date(new Date(endDate).setDate(new Date(endDate).getDate() - 27)).toISOString().slice(0, 10)
            state.selectedDate = [startDate, endDate]
        } else {
            if (newValue !== null && newValue.length === 2 && newValue[0] === null) {
                // Date has been set indirectly (and has the form [null,endDate])
                const endDate = newValue[1]
                const startDate = new Date(new Date(endDate).setDate(new Date(endDate).getDate() - 27)).toISOString().slice(0, 10)
                state.selectedDate = [startDate, endDate]
            } else {
                // Date has been set in another way (either null or [startDate,endDate])
                state.selectedDate = newValue
            }
        }
    },

    setLastUpdate(state,newVal){
        state.lastUpdate=newVal
    }
}