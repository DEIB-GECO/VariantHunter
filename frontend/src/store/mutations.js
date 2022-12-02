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
import {getRandomColor} from "@/utils/colorService";

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
     * Set analysis option
     * @param state
     * @param local     True iff the option has local scope
     * @param opt       Parameter to be set
     * @param value     Value of the parameter
     */
    setOpt(state, {local = true, opt, value}) {
        console.log("setOption of " + opt + " to " + value)
        const id = state.currentAnalysisId

        if (local) {
            Vue.set(state.localOpt[id], opt, value)
        } else {
            const tagName = state.analyses[id].tag
            if (tagName)
                Vue.set(state.tags[tagName], opt, value)
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
     * @param metadata                  Metadata
     */
    addAnalysis(state, {rows, tot_seq, characterizing_muts = null, metadata}) {
        // Save current analysis data
        const endDate = metadata.date

        const pastKeys = Object.keys(state.analyses).map(x=>Number(x))
        const assignedId = pastKeys.length > 0 ? (Math.max(...pastKeys) + 1) : 0

        Vue.set(state.analyses, assignedId, {
            id: assignedId,
            starred: false,
            query: {
                granularity: metadata.location.region === null ? (metadata.location.country === null ? 'continent' : 'country') : 'region',
                location: {
                    continent: metadata.location.continent,
                    country: metadata.location.country,
                    region: metadata.location.region,
                },
                endDate: endDate,
                lineage: metadata.lineage ? metadata.lineage : null,
                weeks: {
                    w1: computeDateLabel(endDate, 27, 21), w2: computeDateLabel(endDate, 20, 14),
                    w3: computeDateLabel(endDate, 13, 7), w4: computeDateLabel(endDate, 6, 0)
                },
                performedOn: new Date().toDateString() + ", " + new Date().toTimeString().slice(0, 5),
                datasetInfo: metadata['dataset_info'],
            },
            notes: null,
            tag: null,
            characterizingMuts: characterizing_muts,
            rows: rows,
            totSeq: {
                w1: tot_seq[0], w2: tot_seq[1], w3: tot_seq[2], w4: tot_seq[3]
            }
        })

        // Preset filtering and ordering options
        Vue.set(state.localOpt, assignedId, {
            useLocalOpt: true,
            protein: null,
            muts: [],
            rowKeys: [],
            sortingIndexes: ["slope"],
            isDescSorting: [true]
        })

        // Show the newly created analysis
        state.currentAnalysisId = assignedId
    },

    setNotes(state, note) {
        Vue.set(state.analyses[state.currentAnalysisId], 'notes', note)
    },

    setTag(state, {analysisId,tagName}){
        console.log("# Set from "+analysisId+" to tag: "+tagName)
        Vue.set(state.analyses[analysisId],'tag',tagName)
    },

    renameTag(state,{newName,oldName}){
        console.log("# Rename from "+oldName+" to "+newName)
        Vue.set(state.tags, newName, state.tags[oldName])
    },

    addTag(state, tagName) {
        console.log("# Add tag " + tagName)
        // New tag? save and assign color
        if (!Object.keys(state.tags).includes(tagName)) {
            Vue.set(state.tags, tagName, {
                tagColor: getRandomColor(),
                createdAt: new Date(),
                protein: null,
                muts: [],
                rowKeys:[],
                sortingIndexes:["slope"],
                isDescSorting:[true]
            })
        }
        Vue.set(state.analyses[state.currentAnalysisId],'tag', tagName)
    },

    deleteTag(state,tagName){
      Vue.delete(state.tags,tagName)
    },

    removeTag(state, tagName) {
        console.log("# Remove tag " + tagName)
        state.analyses[state.currentAnalysisId].tag = null
        state.localOpt[state.currentAnalysisId].useLocalOpt = true
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

        Vue.delete(state.analyses, id)
        Vue.delete(state.localOpt, id)
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


    setTourStep(state,newVal){
        console.log("SET tour to "+newVal)
        state.tourStep=newVal
    },

    setLastUpdate(state, newVal) {
        state.lastUpdate = newVal
    },
    setDatasetInfo(state,info){
        Vue.set(state.datasetInfo,'fileType',info['file_type'])
        Vue.set(state.datasetInfo,'filteredCountries',info['filtered_countries'])
        Vue.set(state.datasetInfo,'beginDate',info['begin_date'])
        Vue.set(state.datasetInfo,'endDate',info['end_date'])
        Vue.set(state.datasetInfo,'parsedOn',info['parsed_on'])
    },

    resetState(state) {
        state.reset = true
    },
    setLoading(state, newVal) {
        state.loading = newVal
    }
}