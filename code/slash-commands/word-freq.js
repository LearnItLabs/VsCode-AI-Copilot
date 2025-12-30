
function countSentences(text) {
    if (!text) {
        return 0;
    }
    const sentences = text.split(/[.!?]+/);
    // Filter out empty strings that can result from splitting
    const nonEmptySentences = sentences.filter(sentence => sentence.trim().length > 0);
    return nonEmptySentences.length;
}

function getWordCounts(text, ignoreWords) {
    const ignoreSet = new Set(ignoreWords.split(',')
        .map(w => w.trim().toLowerCase())
        .filter(w => w.length > 0));
    const words = text
        .toLowerCase()
        .replace(/[\.\,\!\?\;\:\-\(\)\[\]\"\'\r\n\*_“”]/g, ' ')
        .split(/\s+/)
        .filter(w => w.length > 0 && !ignoreSet.has(w));
    const counts = {};
    for (const word of words) {
        counts[word] = (counts[word] || 0) + 1;
    }
    // Convert to array and sort by count descending
    return Object.entries(counts)
        .map(([word, count]) => ({ word, count }))
        .sort((a, b) => b.count - a.count);
}

document.getElementById('analyzeBtn').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');
    const ignoreWords = document.getElementById('ignoreWordsInput').value;
    const resultsDiv = document.getElementById('results');
    const fileNameDiv = document.getElementById('fileName');
    const sentenceCountDiv = document.getElementById('sentenceCount');
    resultsDiv.innerHTML = '';
    fileNameDiv.textContent = '';
    sentenceCountDiv.textContent = '';

    if (!fileInput.files.length) {
        alert('Please select a text file.');
        return;
    }

    const file = fileInput.files[0];
    fileNameDiv.textContent = `Selected file: ${file.name}`;

    const reader = new FileReader();
    reader.onload = function (e) {
        const text = e.target.result;
        const sentenceCount = countSentences(text);
        sentenceCountDiv.textContent = `Number of sentences: ${sentenceCount}`;
        const wordStats = getWordCounts(text, ignoreWords);
        if (wordStats.length === 0) {
            resultsDiv.textContent = 'No words found.';
            return;
        }
        let html = '<table><tr><th>Word</th><th>Count</th></tr>';
        for (const { word, count } of wordStats) {
            html += `<tr><td>${word}</td><td>${count}</td></tr>`;
        }
        html += '</table>';
        resultsDiv.innerHTML = html;
    };
    reader.readAsText(file);
});
