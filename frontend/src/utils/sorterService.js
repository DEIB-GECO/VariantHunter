/**
 *  SORTER SERVICE
 *  It provides sorting functions
 */

import {NotSupportedError} from "core-js/internals/dom-exception-constants";

/**
 * Custom sort function for data table
 * @param items           Array of (processed) rows to be sorted
 * @param sortingIndexes  Array of field names selected for sorting
 * @param isDescSorting   Array of boolean values. Element i is true iff index[i] needs to be desc ordered
 * @returns {Array}       Array of sorted items
 */
export function sortItems(items, sortingIndexes, isDescSorting) {
    // Num of index selected
    const len = sortingIndexes.length

    // No elements to be sorted? Nothing to do
    if (items.length === 0) {
        return items
    }

    // No indexes selected to be sort on? Apply default ones
    if (len === 0) {
        return sortItems(items, ['slope'], [true])
    }

    const positionOfLastIndex = len - 1

    // Sort via custom cmp fn (returning 0 if A==B equal; 1 if A must appear before B; -1 otherwise)
    items.sort(function (a, b) {
        let iLocal = 0
        while (iLocal <= positionOfLastIndex) {
            const consideredIndex = sortingIndexes[iLocal]

            let res  // computed as follows: 0 if A==B, 1 if A<B, -1 if A>B
            switch (typeof (a[consideredIndex])) {
                case "number":
                    res = a[consideredIndex] - b[consideredIndex]
                    break
                case "string":
                    res = a[consideredIndex].localeCompare(b[consideredIndex])
                    break
                default:
                    throw NotSupportedError
            }

            // A<B on the current attribute? No need to check the others.
            if (res > 0) {
                return isDescSorting[iLocal] ? -1 : 1
            }

            // A>B on the current attribute. No need to check the others.
            if (res < 0) {
                return isDescSorting[iLocal] ? 1 : -1
            }

            // A==B on the current attribute. Decide on the basis of the other indexes.
            iLocal++
        }
        // No other indexes selected to be sort on? Then, A==B
        if (iLocal === positionOfLastIndex) {
            return 0
        }
    })
    return items
}