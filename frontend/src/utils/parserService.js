/**
 * PARSER SERVICE
 * It provides general purpose functions to convert formats
 */

/**
 * Converter utility json to csv
 * @param jsonData    The json data to be converted
 * @param headersInfo The headers info for the file to be generated
 * @returns {String}  A string representing the csv file
 */
export function json2csv (jsonData, headersInfo) {
  // Names for the headers of the csv file (es. "Location","Slope",..)
  const fieldsHeaders = []
  // Names of the fields of the jsonData element (es. "location","slope",..)
  const fieldsNames = []

  headersInfo.forEach(function (headerInfo) {
    fieldsHeaders.push(headerInfo.text)
    fieldsNames.push(headerInfo.value)
  })

  const csv = jsonData.map(function (jsonRow) {
    return fieldsNames
      .map(function (fieldName) {
        return JSON.stringify(String(jsonRow[fieldName]))
      })
      .join(',')
  })
  csv.unshift(fieldsHeaders.join(','))
  return csv.join('\r\n')
}

/** Name for downloaded files:  Lin[<LINEAGE>|"Indep"]_<GRANULARITY>_[<LOCATION>]_<DATE> */
export function getFileName(query) {
  return (
      query.location[query.granularity]+"_"+query.endDate+
      (query.lineage? "_"+query.lineage: '')
  )
}