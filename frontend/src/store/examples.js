/**
 * Data for the examples sections
 * {[{
 *      title: title for the example like 'Alpha variant in the UK',
 *      intro: short introductory string for the slider like 'Emergence and spread of the Alpha variant in the UK',
 *      body: long possibly html formatted description of the example,
 *      params: {
 *          granularity: either 'continent', 'country' or 'region'
 *          locationName: location name like 'Europe' or 'Lombardy',
 *          endDate: end date like '2022-01-01'
 *          lineages: null if lineage independent, otherwise: {
 *
 *              items: array of strings representing selected individual lineages like ['BA.1.1','BA.2'] or ['BA.1.11]
 *
 *              groups: object of the form {'groupName':[string]} defining selected group of lineages
 *                      Specify like:
 *                      {
 *                          'BA.1.*': [], # leave the array empty for ease of writing
 *                          'AX.*':[]
 *                      }
 *                      Important: groups must be disjointed!
 *          }
 *      }
 * }]}
 */
export const examples = [
    {
        title: "Alpha variant in the UK",
        intro: "Appearance and spread of the Alpha variant in the UK.",
        body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        params: {
            granularity: 'continent',
            locationName: 'Europe',
            endDate: '2022-01-01',
            lineages: null,
        }
    },
    {
        title: "BA.1.1 lineage in Italy",
        intro: "Appearance and spread of the BA.1.1 lineage in the UK.",
        body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        params: {
            granularity: 'country',
            locationName: 'Italy',
            endDate: '2022-01-01',
            lineages: {
                items: ['BA.1.1'],
                groups: {}
            },
        }
    },
    {
        title: "BA.4.* lineage in Lombardy",
        intro: "Appearance and spread of the BA.4.* lineages in the UK.",
        body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        params: {
            granularity: 'region',
            locationName: 'Lombardy',
            endDate: '2022-01-01',
            lineages: {
                items: [],
                groups: {'BA.4.*':[]}
            },
        }
    },
]