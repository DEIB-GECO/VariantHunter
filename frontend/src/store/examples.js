/**
 * Data for the examples sections
 * {[{
 *      title: title for the example like 'Alpha variant in the UK',
 *      intro: short introductory string for the slider like 'Emergence and spread of the Alpha variant in the UK',
 *      body: long possibly html formatted description of the example,
 *      granularity: either 'continent', 'country' or 'region',
 *      type: either 'ls' (stands for lineage specific) or 'li' (stands for lineage independent)
 *      url: URL obtained from the share function (notice: the part of the URL before '?' is NOT relevant)
 * }]}
 */
export const examples = [
    {
        id: 1,
        title: "Hydra BN.1.9",
        intro: "Emergence of sub-lineage BN.1.9 in October-November 2022",
        granularity: "continent",
        type: "ls",
        url: "cerilab.deib.polimi.it/variant_hunter/linkTo?type=ls&locationName=North%20America&date=2022-11-14&lineages=BN.1",
    },
    {
        id: 2,
        title: "Omicron BA.5.2.39",
        intro: "Emergence of sub-lineage BA.5.2.39 in North America in October-November 2022",
        granularity: "continent",
        type: "ls",
        url: "cerilab.deib.polimi.it/variant_hunter/linkTo?type=ls&locationName=North%20America&date=2022-10-31&lineages=BA.5.2",
    },
    {
        id: 3,
        title: "Omicron BA.4 & BA.5",
        intro: "Spread of the Omicron 4 and 5  variants and displacement of Omicron 1 and 2 variants in North America in May-June 2022",
        granularity: "continent",
        type: "li",
        url: "cerilab.deib.polimi.it/variant_hunter/linkTo?type=li&locationName=North%20America&date=2022-06-11",
    },
    {
        id: 4,
        title: "Omicron BA.1 North America",
        intro: "Spread of the Omicron variant and displacement of the Delta in North America in December 2021",
        granularity: "continent",
        type: "li",
        url: "cerilab.deib.polimi.it/variant_hunter/linkTo?type=li&locationName=North%20America&date=2022-01-01",
    },
    {
        id: 5,
        title: "Omicron BA.1 Europe",
        intro: "Spread of the Omicron variant and displacement of the Delta in Europe in December 2021",
        granularity: "continent",
        type: "li",
        url: "cerilab.deib.polimi.it/variant_hunter/linkTo?type=li&locationName=Europe&date=2022-01-01",
    },
    {
        id: 6,
        title: "Delta B.1.617.2",
        intro: "Early spread of the Delta variant in the UK in April-May 2021",
        granularity: "country",
        type: "li",
        url: "cerilab.deib.polimi.it/variant_hunter/linkTo?type=li&locationName=Europe%2FUnited%20Kingdom&date=2021-05-07",
    },
    {
        id: 7,
        title: "Alpha B.1.1.7",
        intro: "Emergence and spread of the Alpha variant in the UK in October-November 2020",
        granularity: "continent",
        type: "li",
        url: "cerilab.deib.polimi.it/variant_hunter/linkTo?type=li&locationName=Europe%2FUnited%20Kingdom&date=2020-11-22",
    }

]

/** Identifier of the example to be used for the app tour */
export const runExample= 3