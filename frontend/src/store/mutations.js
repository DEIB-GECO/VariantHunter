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

        const pastKeys = Object.keys(state.analyses).map(x => Number(x))
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

    /**
     * Set the notes associated with the current analysis
     * @param state
     * @param note  The notes
     */
    setNotes(state, note) {
        Vue.set(state.analyses[state.currentAnalysisId], 'notes', note)
    },

    /**
     * Set the tag of a specified analysis
     * @param state
     * @param analysisId    The id of the analysis to be considered
     * @param tagName       The tag name to be assigned
     */
    setTag(state, {analysisId, tagName}) {
        Vue.set(state.analyses[analysisId], 'tag', tagName)
    },

    /**
     * Rename an existing tag in the tags list
     * @param state
     * @param newName   New name of the tag
     * @param oldName   Old name of the tag
     */
    renameTag(state, {newName, oldName}) {
        Vue.set(state.tags, newName, state.tags[oldName])
    },

    /**
     * Add a tag to the current analysis.
     * If the tag is a new one, it also creates it
     * @param state
     * @param tagName   Tag name to be assigned
     */
    addTag(state, tagName) {
        // New tag? save and assign color
        if (!Object.keys(state.tags).includes(tagName)) {
            Vue.set(state.tags, tagName, {
                tagColor: getRandomColor(),
                createdAt: new Date(),
                protein: null,
                muts: [],
                rowKeys: [],
                sortingIndexes: ["slope"],
                isDescSorting: [true]
            })
        }
        Vue.set(state.analyses[state.currentAnalysisId], 'tag', tagName)
    },

    /**
     * Delete a tag from the tags list
     * @param state
     * @param tagName   Tag name to be removed
     */
    deleteTag(state, tagName) {
        Vue.delete(state.tags, tagName)
    },

    /**
     * Un-assign the tag of the current analysis and set it to null
     * @param state
     */
    removeTag(state) {
        state.analyses[state.currentAnalysisId].tag = null
        state.localOpt[state.currentAnalysisId].useLocalOpt = true
    },

    /**
     * Remove an analysis given its id
     * @param state
     * @param id        Analysis id
     */
    removeAnalysis(state, id) {
        if (id === state.currentAnalysisId)
            state.currentAnalysisId = null

        Vue.delete(state.analyses, id)
        Vue.delete(state.localOpt, id)
    },

    /**
     * Set the location value in the analysis definition panel
     * @param state
     * @param newValue  The value to be assigned
     */
    setLocation(state, newValue) {
        state.selectedLocation = newValue
    },
    /**
     * Set the possible locations in the analysis definition panel
     * @param state
     * @param newValue  The list of values to be assigned
     */
    setLocations(state, newValue) {
        state.possibleLocations = newValue
    },
    /**
     * Set the information of the possible locations in the analysis definition panel
     * @param state
     * @param newValue  The array of info to be assigned
     */
    setLocationsInfo(state, newValue) {
        state.possibleLocationsInfo = newValue
    },

    /**
     * Set the lineage value in the analysis definition panel
     * @param state
     * @param newValue  The value to be assigned
     */
    setLineage(state, newValue) {
        console.log("setLineage " + newValue)
        state.selectedLineage = newValue
    },
    /**
     * Set the possible lineages in the analysis definition panel
     * @param state
     * @param newValue  The value to be assigned
     */
    setLineages(state, newValue) {
        console.log("setLineages " + newValue)
        state.possibleLineages = newValue
    },
    /**
     * Set the information of the possible lineages in the analysis definition panel
     * @param state
     * @param newValue  The array of info to be assigned
     */
    setLineagesInfo(state, newValue) {
        state.possibleLineagesInfo = newValue
    },

    /**
     * Set the analysis period value in the analysis definition panel
     * @param state
     * @param newValue  The value to be assigned.
     *                  Possible forms: [endDate] , [null,endDate] or [startDate,endDate]
     */
    setDate(state, newValue) {
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

    /**
     * Set the step of the app-tour feature
     * @param state
     * @param newVal    Step name or null value
     */
    setTourStep(state, newVal) {
        state.tourStep = newVal
    },

    /**
     * Set last update date
     * @param state
     * @param newVal    Last update date. Takes format YYYY-mm-dd
     */
    setLastUpdate(state, newVal) {
        state.lastUpdate = newVal
    },
    /**
     * Set the dataset info including 'file_type','filtered_countries',
     * 'begin_date', 'end_date' and 'parsed_on'
     * @param state
     * @param info      Info object
     */
    setDatasetInfo(state, info) {
        Vue.set(state.datasetInfo, 'fileType', info['file_type'])
        Vue.set(state.datasetInfo, 'filteredCountries', info['filtered_countries'])
        Vue.set(state.datasetInfo, 'beginDate', info['begin_date'])
        Vue.set(state.datasetInfo, 'endDate', info['end_date'])
        Vue.set(state.datasetInfo, 'parsedOn', info['parsed_on'])
    },

    /**
     * Set the flag to reset the state. Requires page reload.
     */
    resetState(state) {
        state.reset = true
    },
    /**
     * Set the global loading state
     * @param state
     * @param newVal    The new value
     */
    setLoading(state, newVal) {
        state.loading = newVal
    }
}