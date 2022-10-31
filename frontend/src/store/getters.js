/**
 *
 *  STORE GETTERS METHODS
 *
 *  Usage:        getterName(payload)
 *  Definition:   getterName:(state,getters)=>(payload)=>{}
 *
 **/

export const getters = {
    getAnalysesSummary: (state) => ({mode = null, granularity = null, starred = null}) => {
        console.log("getAnalysesSummary")
        let analyses = state.analyses
        if (starred)
            analyses = analyses.filter(({starred}) => starred)
        if (mode)
            analyses = analyses.filter(({query}) => (mode === 'li' && !query.lineage) || (mode === 'ls' && query.lineage))
        if (granularity)
            analyses = analyses.filter(({query}) => !granularity || granularity === query.granularity)
        return analyses.map(({id, starred, query}) => {
            return {id, starred, query}
        }).sort(({id1}, {id2}) => id1 - id2).reverse()
    },

    getCurrentAnalysis: (state) => {
        console.log("getCurrentAnalysis")
        return state.analyses.find(({id}) => id === state.currentAnalysis)
    },

    getCurrentFilteredRows: (state, getters) => {
        return getters.getCurrentAnalysis.rows
        // console.log("getCurrentFilteredRows")
        // const {useGlobalFilters, filteringOpt} = getters.getCurrentAnalysis
        // const filteredProtein = useGlobalFilters ? state.globalFilteringOpt.protein : filteringOpt.protein
        // const filteredMuts = useGlobalFilters ? state.globalFilteringOpt.muts : filteringOpt.muts
        //
        // return getters.getCurrentAnalysis.rows.filter(({protein, mut}) =>
        //     (filteredProtein === null || protein === filteredProtein) &&
        //     (filteredMuts === null || filteredMuts.length === 0 || filteredMuts.includes(protein + '_' + mut))
        // )
    },
/*
    getCurrentProcessedRows: (state, getters) => {
        const rows = []
        console.log("getCurrentProcessedRows")
        getters.getCurrentFilteredRows.forEach(rawRow => {
            const row = {}

            row['item_key'] = rawRow['protein'] + '_' + rawRow['mut']
            row['location'] = rawRow['location']
            row['protein'] = rawRow['protein']
            row['mut'] = rawRow['mut']

            // Convert numeric slope and p-values into a formatted string
            row['slope'] = rawRow['slope'].toPrecision(4)
            if (!isNaN(rawRow['p_value_with_mut'])) {
                row['p_value_with_mut'] = rawRow['p_value_with_mut'].toExponential(3)
            }
            if (!isNaN(rawRow['p_value_without_mut'])) {
                row['p_value_without_mut'] = rawRow['p_value_without_mut'].toExponential(3)
            }
            if (!isNaN(rawRow['p_value_comp'])) {
                row['p_value_comp'] = rawRow['p_value_comp'].toExponential(3)
            }

            for (let i = 1; i <= 4; i++) {
                row['f_w' + i] = rawRow['f' + i].toPrecision(3) + '% (' + rawRow['w' + i] + ')'
                row['f' + i] = rawRow['f' + i] // numeric value for sorting and plots
                row['w' + i] = rawRow['w' + i] // numeric value for plots
            }

            rows.push(row)
        })
        return rows
    },

    getCurrentSelectedRows: (state,getters) =>{
        const {useGlobalFilters, filteringOpt} = getters.getCurrentAnalysis
        const rows=getters.getCurrentProcessedRows
        const filteredRowKeys = useGlobalFilters ? state.globalFilteringOpt.rowKeys : filteringOpt.rowKeys
        let selectedRows=[]
        if (filteredRowKeys.length > 0)
            selectedRows= rows.filter(({protein, mut}) => filteredRowKeys.includes(protein + '_' + mut))
        else
            selectedRows=[]
        return selectedRows
    },

    getCurrentPlotRows: (state, getters) => {
        const {useGlobalFilters, filteringOpt, rows} = getters.getCurrentAnalysis
        const filteredRowKeys = useGlobalFilters ? state.globalFilteringOpt.rowKeys : filteringOpt.rowKeys
        if (filteredRowKeys.length > 0)
            // return the selected rows
            return rows.filter(({protein, mut}) => filteredRowKeys.includes(protein + '_' + mut))
        else
            return

    },*/
}