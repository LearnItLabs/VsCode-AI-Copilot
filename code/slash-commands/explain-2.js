/**
 * Notes (Big-O):
 prompt: /explain the big o implication of the two functions
 */
function removeDuplicates(arr) {
    const seen = new Set();
    const result = [];
    for (const x of arr) {
        if (!seen.has(x)) {
            seen.add(x);
            result.push(x);
        }
    }
    return result;
}

function removeDuplicatesBySorting(arr) {
    if (arr.length === 0) return [];
    const copy = arr.slice().sort();
    const result = [copy[0]];
    for (let i = 1; i < copy.length; i++) {
        if (copy[i] !== copy[i - 1]) {
            result.push(copy[i]);
        }
    }
    return result;
}
// Example usage:
const sampleArray = [1, 2, 3, 2, 4, 5, 1];
const uniqueArray = removeDuplicates(sampleArray);
console.log("Unique values (O(n)):", uniqueArray);
const uniqueSorted = removeDuplicatesBySorting(sampleArray);
console.log("Unique values (O(n log n), sorted):", uniqueSorted);