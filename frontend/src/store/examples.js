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
        title: "Omicron BA.2.12.1 lineage",
        intro: "Appearance and spread of Omicron BA.2.12.1 lineage in the USA in March 2022.",
        body:
            "<p>From Pango designationissue 499 " +
            "(https://github.com/cov-lineages/pango-designation/issues/499) , which led to " +
            "the definition of the BA.2.12.1 sublineage of SARS-CoV-2.</p>" +
            "<p>The novel lineage is defined by a L452Q amino acid change in the spike glycoprotein " +
            "according to the submitter.</p>" +
            "<p>A clear increase in the prevalence of L452Q within lineage BA.2.12.1 is observed " +
            "both from the Diffusion Odds Ratio plot and the Diffusion Heatmap. </p>" +
            "<p>As outlined from the Diffusion Odds Ratio plot the amino acid change that defines " +
            "the new lineage seems to be associated with a clear growth advantage.</p>",
        type: 'ls',
        granularity: 'country',
        url: '.../linkTo?type=ls&locationName=North%20America%2FUSA&date=2022-03-30&lineages=BA.2.12&lineages=BA.2.12.1',
    },
    {
        title: "Omicron variant in Europe",
        intro: "Spread of the Omicron variant and displacement of the Delta in Europe in December 2022.",
        body:
            "<p>A \"lineage-independent\" analysis was applied to study the prevalence of amino acid " +
            "changes in the Spike glycoprotein in an interval of time spanning from 05/12/2021 to " +
            "01/01/2022 in Europe.</p><p>This interval coincides the rapid emergence and spread of " +
            "the Omicron variant of SARS-CoV-2 worldwide.</p>" +
            "<p>A clear decrease in the prevalence of 6 amino acid changes characteristic of the " +
            "Delta variant(L452R, P681R, D950N, R158G, S478K, T19R) and a concomitant and striking " +
            "increase of 23 amino acid changes associated with the Omicron variant of SARS-CoV-2 " +
            "is observed</p>" +
            "<p>Equivalent patterns are recovered both from the Diffusion Heatmap and Diffusion Trend Chart.</p>",
        granularity: 'continent',
        type: 'li',
        url: '.../linkTo?type=li&locationName=Europe&date=2022-01-01',
    },
    {
        title: "Omicron BA.1.15.2 lineage",
        intro: "Appearance and spread of Omicron BA.1.15.2 lineage in the USA in March 2022.",
        body:
            "<p>From Pango designationissue 508 " +
            "(https://github.com/cov-lineages/pango-designation/issues/508) , which led to " +
            "the definition of the BA.1.15.2 sublineage of SARS-CoV-2.</p>" +
            "<p>The novel lineage is defined by a Q628K amino acid change in the spike glycoprotein " +
            "according to the submitter. </p>" +
            "<p>A clear increase in the prevalence of Q628K within lineage BA.1.15.2 is observed " +
            "both from the Diffusion Odds Ratio plot and the Diffusion Heatmap.</p>",
        granularity: 'country',
        type: 'ls',
        url: '.../linkTo?type=ls&locationName=North%20America%2FUSA&date=2022-03-30&lineages=BA.1.15&lineages=BA.1.15.2',
    },
    {
        title: "Alpha variant in the United Kingdom",
        intro: "Appearance and spread of the Alpha variant in the UK in November 2020.",
        body:
            "<p>This interval of time corresponds with the emergence and spread of the Alpha " +
            "variant in the UK. </p><p>As illustrated by the Mutation table and the Diffusion Heatmap, " +
            "6 amino acid changes in the Spike glycoprotein are singled out due to remarkable " +
            "increase in frequency (from 1% to 11%).</p>" +
            "<p>Similar patterns of increase in frequency of the 6 selected amino acid changes can " +
            "be observed also from the Diffusion Trend Chart and Diffusion Odds Ratio plots.</p>",
        granularity: 'country',
        type: 'li',
        url: '.../linkTo?type=li&locationName=Europe%2FUnited%20Kingdom&date=2020-11-16',
    },

]