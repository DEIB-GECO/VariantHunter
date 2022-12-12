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
        title: "Alpha variant in the UK",
        intro: "Appearance and spread of the Alpha variant in the UK.",
        body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        type: 'ls',
        granularity: 'continent',
        url: 'NOT_RELEVANT/variant_hunter/linkTo?type=ls&location=11&date=2022-10-14&lineages=BA.4.1&lineages=BA.2.%2a',
    },
    {
        title: "BA.1.1 lineage in Italy",
        intro: "Appearance and spread of the BA.1.1 lineage in the UK.",
        body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        granularity: 'country',
        type: 'li',
        url: 'NOT_RELEVANT/variant_hunter/linkTo?type=li&location=11&date=2022-10-14',
    },
    {
        title: "BA.4.* lineage in Lombardy",
        intro: "Appearance and spread of the BA.4.* lineages in the UK.",
        body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        granularity: 'region',
        type: 'ls',
        url: 'NOT_RELEVANT/variant_hunter/linkTo?type=ls&location=11&date=2022-10-14&lineages=BA.4.1',
    },
]