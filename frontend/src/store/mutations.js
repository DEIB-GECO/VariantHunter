/**
 *
 *  STORE MUTATIONS METHODS
 *
 *  Usage:        commit('mutationName',payload)
 *  Definition:   mutationName(state,payload){}
 *
 **/

export const mutations={
    setCurrentAnalysis(state,id){
        console.log("setCurrentAnalysis to "+id)
        state.currentAnalysis=id
    },

    setStarredAnalysis(state,{id,starred=true}){
        console.log("setStarredAnalysis of "+id+" to "+starred)
        state.analyses[id].starred=starred
    },

    removeAnalysis(state,id){
        console.log("removeAnalysis "+id)
        const index = state.analyses.findIndex(({id:analysisId})=>id===analysisId);
        if (index > -1) {
          state.analyses.splice(index, 1);
        }
    }
}