/**
 *  COLOR SERVICE
 *  It provides colors utilities
 */

/**
 * Determine whether a color is light or dark
 * @param bgColor         Color to be checked
 * @returns {string}    Either 'dark' or 'light'
 */
function lightOrDark(bgColor) {
    var color = (bgColor.charAt(0) === '#') ? bgColor.substring(1, 7) : bgColor;
    var r = parseInt(color.substring(0, 2), 16); // hexToR
    var g = parseInt(color.substring(2, 4), 16); // hexToG
    var b = parseInt(color.substring(4, 6), 16); // hexToB
    var uicolors = [r / 255, g / 255, b / 255];
    var c = uicolors.map((col) => {
        if (col <= 0.03928) {
            return col / 12.92;
        }
        return Math.pow((col + 0.055) / 1.055, 2.4);
    });
    var L = (0.2126 * c[0]) + (0.7152 * c[1]) + (0.0722 * c[2]);
    return (L > 0.179) ? 'light' : 'dark';
}

/**
 * Gets a random color
 * @returns {Object}    Object describing color code and color brightness
 */
export function getRandomColor() {
    const colorCode = '#' + (Math.random() * 0xFFFFFF << 0).toString(16)
    const isDark = lightOrDark(colorCode) === 'dark'
    return {color: colorCode, isDark}
}

/**
 * Test color brightness
 * @param colorCode     Color string
 * @returns {Boolean}    True iff the color is dark one
 */
export function isDark(colorCode) {
    const isDark = lightOrDark(colorCode) === 'dark'
    return isDark
}

/**
 * Get location color based on granularity
 * @param granularity Granularity value
 * @returns {string}  Color code
 */
export function getLocationColor(granularity) {
    return granularity === 'region'
        ? '#7CB17B'
        : granularity === 'country'
            ? '#ff6e3e'
            : '#90177d'
}

/** Colors for plots */
export const palette = [
    '#bbef39', '#29b7d5', '#f3df67', '#6685f1',
    '#2fd901', '#ff3f00', '#003aff', '#ff6200',
    '#ef8f4b', '#d46ff5', '#4fcbe7', '#ffb600',
    '#ff1cb6', '#9a02ff', '#00fff7', '#333333',
    '#ef5378', '#fcb0ca', '#7ed7cd', '#ef479e',
    '#ffbc73', '#fffac8', '#c56100', '#95e0ab',
    '#808000', '#ffd8b1', '#601e1e', '#72ee84',
    '#058011', '#6b6868', '#b2b2b2', '#000000'
]