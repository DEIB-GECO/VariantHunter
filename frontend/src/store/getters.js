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
        // Returns a time-sorted summary for each analysis
        return Object.values(state.analyses)
            .map(({id, starred, query, tag}) => ({id, starred, query, tag}))
            .sort(({id1}, {id2}) => id1 - id2).reverse()
    },

    /** Gets the currently displayed analysis */
    getCurrentAnalysis: (state) => {
        return state.analyses[state.currentAnalysisId]
    },

    /** Gets the local opts of the currently displayed analysis */
    getCurrentLocalOpt: (state) => {
        return state.localOpt[state.currentAnalysisId]
    },


    /** Gets the tag opts of the currently displayed analysis */
    getCurrentTagOpt: (state) => {
        if (state.currentAnalysisId === null) return undefined

        const tag = state.analyses[state.currentAnalysisId].tag
        if (tag)
            return state.tags[tag]
    },

    /** Gets the opts of the currently displayed analysis */
    getCurrentOpt: (state, getters) => {
        return (getters.useLocalOpt) ? getters.getCurrentLocalOpt : getters.getCurrentTagOpt
    },


    /** Gets the local filtering flag of the currently displayed analysis */
    useLocalOpt: (state) => {
        if (state.currentAnalysisId === null) return undefined

        return state.localOpt[state.currentAnalysisId].useLocalOpt
    },

    /**
     * Gets the rows of the current analysis that satisfy protein and mutations filters.
     * To be shown on the table
     */
    getCurrentFilteredRows: (state, getters) => {
        if (state.currentAnalysisId === null) return undefined
        const {protein: filteredProtein, muts: filteredMuts} = getters.getCurrentOpt

        return getters.getCurrentAnalysis.rows.filter(({protein, item_key}) =>
            (filteredProtein === null || protein === filteredProtein) &&
            (filteredMuts === null || filteredMuts.length === 0 || filteredMuts.includes(item_key))
        )
    },

    /**
     * Gets the currently selected rows of the table. They must also satisfy the
     * protein and muts filtering options.
     */
    getCurrentSelectedRows: (state, getters) => {
        if (state.currentAnalysisId === null) return undefined
        const {rowKeys: filteredRowKeys} = getters.getCurrentOpt

        let selectedRows = []
        if (filteredRowKeys.length > 0) {
            const rows = getters.getCurrentFilteredRows
            selectedRows = rows.filter(({item_key}) => filteredRowKeys.includes(item_key))
        } else
            selectedRows = []
        return selectedRows
    },

    /**
     * Get plot data as an object as follows {'title': title of the plot, 'rows': array or mutations}
     * Specifically the mutations are those that have been selected by the user or the top 5
     * increasing + top 5 decreasing mutations if no rows have been selected
     */
    getCurrentPlotInfo: (state, getters) => {
        if (state.currentAnalysisId === null) return undefined
        const {rowKeys: filteredRowKeys, sortingIndexes, isDescSorting} = getters.getCurrentOpt
        let title, rows

        if (filteredRowKeys.length > 0) {
            // User selected rows only (keep same ordering criteria)
            title = `Selected mutations (${filteredRowKeys.length})`
            rows = sortItems(getters.getCurrentSelectedRows, sortingIndexes, isDescSorting).reverse()
        } else {
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
        return {title, rows}
    },

    /**
     * Shortcut for plot rows
     */
    getCurrentPlotRows: (state, getters) => {
        if (state.currentAnalysisId === null) return undefined

        return getters.getCurrentPlotInfo.rows
    },

    /**
     * Shortcut for plot title
     */
    getCurrentPlotTitle: (state, getters) => {
        if (state.currentAnalysisId === null) return undefined

        return getters.getCurrentPlotInfo.title
    },

    /**
     * Get the currently selected lineage values (items + group values)
     */
    getSelectedLineageValues: (state) => {
        const list = [...state.selectedLineage.items]
        Object.values(state.selectedLineage.groups).forEach(group => list.push(...group))
        return list
    },
    /**
     * Get the currently selected lineage values (items + group keys)
     */
    getSelectedLineage: (state) => {
        const list = [...state.selectedLineage.items]
        list.push(...Object.keys(state.selectedLineage.groups))
        return list
    }

}