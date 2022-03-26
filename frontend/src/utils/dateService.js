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
