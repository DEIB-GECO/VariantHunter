/**
 * Compute the table label for the week based on the day difference from the reference date
 * @param endDate     Reference date
 * @param from        Difference from the reference date for the start date of the label
 * @param to          Difference from the reference date for the ending date of the label
 * @returns {string}  A string of the form "YYYY/mm/dd - YYYY/mm/dd"
 */
export function computeDateLabel(endDate,from, to) {
    const referenceDate = new Date(endDate)
    const fromDate = new Date(referenceDate)
    const toDate = new Date(referenceDate)

    fromDate.setDate(referenceDate.getDate() - from)
    toDate.setDate(referenceDate.getDate() - to)
    return (
        fromDate
            .toISOString()
            .slice(0, 10)
            .replaceAll('-', '/') +
        ' - ' +
        toDate
            .toISOString()
            .slice(0, 10)
            .replaceAll('-', '/')
    )
}