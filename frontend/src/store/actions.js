/**
 *
 *  STORE ACTIONS METHODS
 *
 *  Usage:        dispatch('actionName',payload)
 *  Definition:   actionName({commit,dispatch,getters,state},payload){}
 *
 **/

export const actions = {

    /**
     * Clear all the analysis and set current analysis to null
     */
    clearHistory({commit, state}) {
        return new Promise(resolve => {
            commit('setCurrentAnalysis', null)
            Object.keys(state.analyses).forEach(id => commit('removeAnalysis', id))
            resolve()
        })
    },

    /**
     * Adds a new analysis related to the current one. Specifically: if the current analysis has no tag, a new one is generated that is assigned to the current analysis and the new analysis;
     * In this case the local filtering options are copied into the tag based scope .
     * On the other hand, if the current analysis has specified a tag then the tag is also applied to the new analysis.
     * @param storeObj
     * @param payload   The new analysis payload
     */
    addGroupAnalysis({commit, state, getters}, payload) {
        return new Promise(resolve => {
            // Before adding new analysis verify tag existence.
            let currTag = state.analyses[state.currentAnalysisId].tag
            let enableTag = false
            if (!currTag) {
                // If not existing, create and assign one
                const existingTags = Object.keys(state.tags)
                let idx = 1
                currTag = 'TAG ' + idx
                while (existingTags.includes(currTag)) {
                    idx++
                    currTag = 'TAG ' + idx
                }
                enableTag = true
                commit('addTag', currTag)

                // Copy the local options into the tag options
                const localOpt = getters.getCurrentLocalOpt
                localOpt.useLocalOpt = false // force tag based filtering
                Object.entries(localOpt)
                    .forEach(([opt, value]) => commit('setOpt', {local: opt === 'useLocalOpt', opt, value}))
            } else {
                enableTag = !getters.useLocalOpt
            }

            // Actually add new analysis and shift to it. Then assign the previously created tag
            commit('addAnalysis', payload)
            commit('addTag', currTag)
            // Enable tag options only if previously enabled or tag was not existing
            if (enableTag)
                commit('setOpt', {local: true, opt: 'useLocalOpt', value: false})
            resolve()
        })
    },

    /**
     * Add a new analysis and assign it a tag if specified
     * @param storeObj
     * @param rows                  Rows data
     * @param tot_seq               Tot seq data
     * @param characterizing_muts   Characterizing mutations data
     * @param metadata              Metadata
     * @param tag                   Tag to be assigned or null value
     */
    addAnalysis({commit}, {rows, tot_seq, characterizing_muts = null, metadata, tag}) {
        return new Promise(resolve => {
            commit('addAnalysis', {rows, tot_seq, characterizing_muts, metadata})
            if (tag)
                commit('addTag', tag)
            resolve()
        })
    },

    /**
     * Rename an existing tag or create a new one if not existing
     * @param storeObj
     * @param newName   The new name of the tag
     * @param oldName   The old name of an existing tag. If not existing, a new tag will be created
     */
    updateTagName({commit, state, getters}, {newName, oldName}) {
        return new Promise(resolve => {
            newName = newName.toUpperCase()

            // New tag: create it
            if (!Object.keys(state.tags).includes(newName)) {
                commit('renameTag', {oldName, newName})
            }
            // replace and delete old one
            getters.getAnalysesSummary
                .filter(({tag}) => tag === oldName)
                .forEach(({id}) => commit('setTag', {analysisId: id, tagName: newName}))
            commit('deleteTag', oldName)
            resolve()
        })
    }

}