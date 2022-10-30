/**
 *
 *  STORE GETTERS METHODS
 *
 *  Usage:        getterName(payload)
 *  Definition:   getterName:(state,getters)=>(payload)=>{}
 *
 **/

export const getters={
    getAnalysesSummary: (state)=>({mode=null, granularity=null, starred=null})=>{
        console.log("getAnalysesSummary")
        let analyses=state.analyses
        if (starred)
            analyses=analyses.filter(({starred})=> starred)
        if (mode)
            analyses=analyses.filter(({query})=> (mode==='li' && !query.lineage) || (mode==='ls' && query.lineage))
        if (granularity)
            analyses=analyses.filter(({query})=> !granularity || granularity===query.granularity)
        return analyses.map(({id,starred,query})=>{return {id, starred, query}}).sort(({id1},{id2})=>id1-id2).reverse()
    },

    getCurrentAnalysis: (state)=>{
        return state.analyses.find(({id})=>id===state.currentAnalysis)
    }
}