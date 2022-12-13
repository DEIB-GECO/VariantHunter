/**
 *  KEYBOARD SERVICE
 *  It provides supported shortcuts info
 */

/**
 * Object defining supported shortcuts
 * @type {{"0": {title: string, kbd: string[]}, "1": {title: string, kbd: string[]}, "2": {title: string, kbd: string[]}}}
 */
export const shortcuts = {
    0: {
        title: 'New analysis',
        kbd: ['<kbd>CTRL</kbd>', ' <kbd>N</kbd>'],
    },
    1: {
        title: 'Prev analysis',
        kbd: ['<kbd>CTRL</kbd>', '<kbd>&uarr;</kbd>'],
    },
    2: {
        title: 'Next analysis',
        kbd: ['<kbd>CTRL</kbd>', '<kbd>&darr;</kbd>'],
    }
}