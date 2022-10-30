/**
 *
 *  STORE MUTATIONS METHODS
 *
 *  Usage:        commit('mutationName',payload)
 *  Definition:   mutationName(state,payload){}
 *
 **/

import {computeDateLabel} from "@/store/utils/utils";

let nextAnalysisId = 2

export const mutations = {
    setCurrentAnalysis(state, id) {
        console.log("setCurrentAnalysis to " + id)
        state.currentAnalysis = id
    },

    setStarredAnalysis(state, {id, starred = true}) {
        console.log("setStarredAnalysis of " + id + " to " + starred)
        const index = state.analyses.findIndex(({id: analysisId}) => id === analysisId);
        if (index > -1) {
            state.analyses[index].starred = starred
        }

    },

    addAnalysis(state, {rows, tot_seq, characterizing_muts, mode}) {
        console.log("addAnalysis "+nextAnalysisId)
        console.log(tot_seq)
        console.log(characterizing_muts)
        console.log(mode)

        const locationInfo=state.possibleLocationsInfo[state.selectedLocation]
        const endDate=state.selectedDate[1]
        console.log(state.analyses.push({
            id: nextAnalysisId,
            starred: false,
            query: {
                granularity: locationInfo.type,
                location: {
                    continent: locationInfo.type==='continent'?state.selectedLocation:locationInfo.continent,
                    country: locationInfo.type==='country'?state.selectedLocation:locationInfo.country,
                    region: locationInfo.type==='region'?state.selectedLocation:null,
                },
                endDate: endDate,
                lineage: mode==='ls'?state.selectedLineage:null,
                weeks: {
                    w1: computeDateLabel(endDate,27, 21), w2: computeDateLabel(endDate,20, 14),
                    w3: computeDateLabel(endDate,13, 7), w4: computeDateLabel(endDate,6, 0)
                }
            },
            useGlobalFilters: true,
            filteringOpt: {protein:null, muts:[],rowKeys:[]},
            characterizingMuts: characterizing_muts,
            muts: rows,
            totSeq: {
                w1: tot_seq[0], w2: tot_seq[1], w3: tot_seq[2], w4: tot_seq[3]
            }
        }))
        state.currentAnalysis=nextAnalysisId
        nextAnalysisId++
    },

    removeAnalysis(state, id) {
        console.log("removeAnalysis " + id)
        if(id===state.currentAnalysis) state.currentAnalysis=null

        const index = state.analyses.findIndex(({id: analysisId}) => id === analysisId);
        if (index > -1) {
            state.analyses.splice(index, 1);
        }
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
}