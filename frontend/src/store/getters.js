/**
 *
 *  STORE GETTERS METHODS
 *
 *  Usage:        getterName(payload)
 *  Definition:   getterName:(state,getters)=>(payload)=>{}
 *
 **/
import {sortItems} from "@/utils/sorterService";

export const getters = {
    /**
     * Gets a summary of the past analysis
     */
    getAnalysesSummary: (state) => {
        console.log("getAnalysesSummary")
        // Returns a time-sorted summary for each analysis
        return Object.values(state.analyses)
            .map(({id, starred, query}) => ({id, starred, query}))
            .sort(({id1}, {id2}) => id1 - id2).reverse()
    },

    /** Gets the currently displayed analysis */
    getCurrentAnalysis: (state) => {
        console.log("getCurrentAnalysis")
        return state.analyses[state.currentAnalysisId]
    },

    /** Gets the local opts of the currently displayed analysis */
    getCurrentLocalOpt: (state) => {
        console.log("getCurrentLocalOpt")
        return state.localOpt[state.currentAnalysisId]
    },


    /** Gets the tag opts of the currently displayed analysis */
    getCurrentTagOpt: (state) => {
        if(state.currentAnalysisId===null) return undefined

        console.log("getCurrentTagOpt")
        const tag = state.analyses[state.currentAnalysisId].tag
        if(tag)
            return state.tags[tag]
    },

    /** Gets the opts of the currently displayed analysis */
    getCurrentOpt: (state,getters) => {
        console.log("getCurrentOpt")
        return (getters.useLocalOpt)? getters.getCurrentLocalOpt : getters.getCurrentTagOpt
    },


    /** Gets the local filtering flag of the currently displayed analysis */
    useLocalOpt: (state) => {
        if(state.currentAnalysisId===null) return undefined

        console.log("useLocalOpt")
        return state.localOpt[state.currentAnalysisId].useLocalOpt
    },

    /**
     * Gets the rows of the current analysis that satisfy protein and mutations filters. To be shown on the table
     */
    getCurrentFilteredRows: (state, getters) => {
        if(state.currentAnalysisId===null) return undefined
        const {protein:filteredProtein,muts:filteredMuts} = getters.getCurrentOpt

        return getters.getCurrentAnalysis.rows.filter(({protein, mut}) =>
            (filteredProtein === null || protein === filteredProtein) &&
            (filteredMuts === null || filteredMuts.length === 0 || filteredMuts.includes(protein + '_' + mut))
        )
    },

    /**
     * Gets the currently selected rows of the table. They must also satisfy the protein and muts filtering options.
     */
    getCurrentSelectedRows: (state,getters) =>{
        if(state.currentAnalysisId===null) return undefined
        const {rowKeys:filteredRowKeys} = getters.getCurrentOpt

        let selectedRows=[]
        if (filteredRowKeys.length > 0) {
            const rows=getters.getCurrentFilteredRows
            selectedRows = rows.filter(({protein, mut}) => filteredRowKeys.includes(protein + '_' + mut))
        } else
            selectedRows=[]
        return selectedRows
    },

    getCurrentPlotInfo: (state, getters) => {
        if(state.currentAnalysisId===null) return undefined
        const {rowKeys:filteredRowKeys,sortingIndexes, isDescSorting} = getters.getCurrentOpt
        let title, rows

        if (filteredRowKeys.length > 0){
            // User selected rows only (keep same ordering criteria)
            title = `Selected mutations (${filteredRowKeys.length})`
            rows = sortItems(getters.getCurrentSelectedRows,sortingIndexes,isDescSorting).reverse()
        } else{
            // Top 10 mutations only

             const sortedRows = sortItems(getters.getCurrentFilteredRows, ['slope'], [false])
            if (sortedRows.length >= 10) {
              title = 'Top 5 <span class="success--text font-weight-bold">increasing</span> and top 5 <span class="error--text font-weight-bold">decreasing</span> mutations'
              rows = sortedRows.slice(0, 5).concat(sortedRows.slice(-5))
            } else {
              title = `All mutations (${sortedRows.length})`
              rows = sortedRows
            }
        }
        return {title,rows}
    },

    getCurrentPlotRows: (state, getters) => {
        if(state.currentAnalysisId===null) return undefined

        return getters.getCurrentPlotInfo.rows
    },

    getCurrentPlotTitle: (state, getters) => {
        if(state.currentAnalysisId===null) return undefined
        
        return getters.getCurrentPlotInfo.title
    },

}