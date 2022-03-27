/**
 * DATE SERVICE
 * It provides general purpose date transformations
 */

/**
 * Reference starting date for the database
 * @type {Date}
 */
export const startDate = new Date('2020-01-01')

/**
 * Compute the date from the date difference value wrt to the start date
 * @param dateDiff  The value of the date diff
 * @returns {Date}  The actual date
 */
export function diffToDate (dateDiff) {
  const date = new Date(startDate)
  // Dates from the server are relative and must be added to the start date
  date.setDate(startDate.getDate() + dateDiff)
  return date
}

/**
 * Compute difference in days between two dates
 * @param date1   String of the first date
 * @param date2   String of the second date
 * @returns {number}
 */
export function dateDiff (date1, date2) {
  const d1 = new Date(date1)
  const d2 = new Date(date2)
  const diff = d2.getTime() - d1.getTime()
  return diff / (1000 * 60 * 60 * 24)
}
