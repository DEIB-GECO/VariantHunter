/**
 * FORMATTER SERVICE
 * It provides general purpose formatter services to summarize lineages data
 */

export function compactLineagesData (lineagesData,level=1){

    // Compute the lineages in star notation
    const regExp=level===1
        ? (/^([a-zA-Z0-9]+.[a-zA-Z0-9]+|[[a-zA-Z0-9]+)/gm) // aggregate at level 1 (A.1.*)
        :(/^([a-zA-Z0-9]+.[a-zA-Z0-9]+.[a-zA-Z0-9]+|[a-zA-Z0-9]+.[a-zA-Z0-9]+|[[a-zA-Z0-9]+)/gm)  // aggregate at level 2 (A.1.2.*)
    const lineagesNames = new Set(lineagesData.map(({name})=>name.match(regExp).at(0)))

    const compData=[]
    // Compute the aggregated counts for the lineages in star notation by summing up
    lineagesNames.forEach(compName=>{
        const initialValue={name:compName,f1:0,f2:0,f3:0,f4:0,w1:0,w2:0,w3:0,w4:0,rows:-1}
        let expName
        const aggregatedValue=lineagesData
            .filter(({name})=>name.startsWith(compName))
            .reduce((p,c)=>{
                expName=c.name
                return {
                    name:p.name,
                    f1:p.f1+c.f1, f2:p.f2+c.f2, f3:p.f3+c.f3, f4:p.f4+c.f4,
                    w1:p.w1+c.w1, w2:p.w2+c.w2, w3:p.w3+c.w3, w4:p.w4+c.w4,
                    rows: (p.rows|0)+(c.rows|0)+1
                }}, initialValue)

        if(aggregatedValue.rows>0)
            aggregatedValue.name+='.*' // correct name with * notation if rows have been aggregated
        else
            aggregatedValue.name= expName  // restore expanded notation if no rows have been aggregated

        compData.push(aggregatedValue)
    })

    return compData
}
