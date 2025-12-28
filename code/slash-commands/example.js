function findDuplicates(arr) {
    for (let i = 0; i < arr.length; i++) {
        for (let j = i + 1; j < arr.length; j++) {
            if (arr[i] === arr[j]) {
                console.log("Duplicate:", arr[i]);
            }
        }
    }
}
// Example usage:
const sampleArray = [1, 2, 3, 2, 4, 5, 1];
findDuplicates(sampleArray);