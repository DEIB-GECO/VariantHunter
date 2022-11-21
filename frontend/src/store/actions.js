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
    }
}