/**
 *  BIND SERVICE
 *  It provides binding functionalities to the $state
 */

/**
 * Performs two-way mapping to vuex state by generating computed
 * properties with getters and setters for the specified state variables
 * @param args      Object of state_var_name: 'MUTATION_NAME'
 * @returns {{}|*}  Set of computed properties with setter and getters
 */
export function mapStateTwoWay(...args) {
    const result = {}

    if (args.length === 1) {
        for (const prop of Object.keys(args[0])) {
            result[prop] = {
                get() {
                    return this.$store.state[prop]
                },
                set(value) {
                    this.$store.commit(args[0][prop], value)
                }
            }
        }
    } else {
        for (const prop of Object.keys(args[1])) {
            result[prop] = {
                get() {
                    return this.$store.state[args[0]][prop]
                },
                set(value) {
                    this.$store.commit(args[0] + '/' + args[1][prop], value)
                }
            }
        }
    }

    return result
}
