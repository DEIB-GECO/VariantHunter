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
     * Gets a summary of the past analysis filtered by mode, granularity and/or starred flag
     */
    getAnalysesSummary: (state) => ({mode = null, granularity = null, starred = null}) => {
        console.log("getAnalysesSummary")
        let analyses = Object.values(state.analyses)

        // Apply filtering parameters
        if (starred)
            analyses = analyses.filter(({starred}) => starred)
        if (mode)
            analyses = analyses.filter(({query}) => (mode === 'li' && !query.lineage) || (mode === 'ls' && query.lineage))
        if (granularity)
            analyses = analyses.filter(({query}) => !granularity || granularity === query.granularity)

        // Returns a time-sorted summary for each analysis
        return analyses
            .map(({id, starred, query}) => ({id, starred, query}))
            .sort(({id1}, {id2}) => id1 - id2).reverse()
    },

    /** Gets the currently displayed analysis */
    getCurrentAnalysis: (state) => {
        console.log("getCurrentAnalysis")
        return state.analyses[state.currentAnalysisId]
    },

    /** Gets the local filtering opts of the currently displayed analysis */
    getCurrentLocalFilteringOpt: (state) => {
        console.log("getCurrentLocalFilteringOpt")
        return state.localFilteringOpt[state.currentAnalysisId]
    },

    /** Gets the local ordering opts of the currently displayed analysis */
    getCurrentLocalOrderingOpt: (state) => {
        console.log("getCurrentLocalOrderingOpt")
        return state.localOrderingOpt[state.currentAnalysisId]
    },

    /**
     * Gets the rows of the current analysis that satisfy protein and mutations filters. To be shown on the table
     */
    getCurrentFilteredRows: (state, getters) => {
        console.log("getCurrentFilteredRows")
        const {useGlobalFilters, ...localFilteringOpt} = getters.getCurrentLocalFilteringOpt
        const filteredProtein = useGlobalFilters ? state.globalFilteringOpt.protein : localFilteringOpt.protein
        const filteredMuts = useGlobalFilters ? state.globalFilteringOpt.muts : localFilteringOpt.muts

        return getters.getCurrentAnalysis.rows.filter(({protein, mut}) =>
            (filteredProtein === null || protein === filteredProtein) &&
            (filteredMuts === null || filteredMuts.length === 0 || filteredMuts.includes(protein + '_' + mut))
        )
    },

    /**
     * Gets the currently selected rows of the table. They must also satisfy the protein and muts filtering options.
     */
    getCurrentSelectedRows: (state,getters) =>{
        const {useGlobalFilters, rowKeys} = getters.getCurrentLocalFilteringOpt
        const filteredRowKeys = useGlobalFilters ? state.globalFilteringOpt.rowKeys : rowKeys

        let selectedRows=[]
        if (filteredRowKeys.length > 0) {
            const rows=getters.getCurrentFilteredRows
            selectedRows = rows.filter(({protein, mut}) => filteredRowKeys.includes(protein + '_' + mut))
        } else
            selectedRows=[]
        return selectedRows
    },

    getCurrentPlotInfo: (state, getters) => {
        const {useGlobalFilters, rowKeys} = getters.getCurrentLocalFilteringOpt
        const filteredRowKeys = useGlobalFilters ? state.globalFilteringOpt.rowKeys : rowKeys
        const {sortingIndexes, isDescSorting} = useGlobalFilters ? state.globalOrderingOpt : getters.getCurrentLocalOrderingOpt
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
        return getters.getCurrentPlotInfo.rows
    },

    getCurrentPlotTitle: (state, getters) => {
        return getters.getCurrentPlotInfo.title
    },

}