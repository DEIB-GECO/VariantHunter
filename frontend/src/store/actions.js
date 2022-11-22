/**
 *
 *  STORE ACTIONS METHODS
 *
 *  Usage:        dispatch('actionName',payload)
 *  Definition:   actionName({commit,dispatch,getters,state},payload){}
 *
 **/

export const actions={

    clearHistory({commit,state}){
        return new Promise(resolve => {
            Object.keys(state.analyses).forEach(id => commit('removeAnalysis', id))
            resolve()
        })
    },

    addGroupAnalysis({commit,state,getters},payload){
        return new Promise(resolve => {
            // Before adding new analysis verify tag existence.
            let currTag = state.analyses[state.currentAnalysisId].tag
            let enableTag = false
            if(!currTag){
                // If not existing, create and assign one
                const existingTags = Object.keys(state.tags)
                let idx = 1
                currTag = 'TAG '+idx
                while(existingTags.includes(currTag)){
                    idx ++
                    currTag = 'TAG '+idx
                }
                enableTag = true
                commit('addTag',currTag)

                // Copy the local options into the tag options
                const localOpt=getters.getCurrentLocalOpt
                localOpt.useLocalOpt = false // force tag based filtering
                Object.entries(localOpt)
                    .forEach(([opt,value])=> commit('setOpt',{local:opt==='useLocalOpt',opt,value}))
            }else{
                enableTag = !getters.useLocalOpt
            }

            // Actually add new analysis and shift to it. Then assign the previously created tag
            commit('addAnalysis', payload)
            commit('addTag', currTag)
            // Enable tag options only if previously enabled or tag was not existing
            if(enableTag)
                commit('setOpt',{local:true,opt:'useLocalOpt',value:false})
            resolve()
        })
    },

    addAnalysis({commit}, {rows, tot_seq, characterizing_muts = null, metadata, tag}) {
        return new Promise(resolve => {
            commit('addAnalysis',{rows, tot_seq, characterizing_muts, metadata})
            if(tag)
                commit('addTag',tag)
             resolve()
        })
    }

}