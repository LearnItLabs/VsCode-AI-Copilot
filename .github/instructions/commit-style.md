Here is exactly what that Markdown file should look like to match your specific requirements.

Because this is a Custom Instructions file for the commit generator, you can use plain English and simple Markdown formatting. Copilot reads this as its "Rulebook" every time you click that sparkle icon.

The Markdown File Content
Save this as .github/instructions/commit-style.md:

Markdown

# Git Commit Message Instructions

## Structure
1. **Summary Paragraph**: Always start with a short, 1-2 sentence paragraph at the top summarizing the high-level purpose of the changes.
2. **Change List**: Use a bulleted list to describe each individual change. 
   - Each bullet must start with a relevant emoji (e.g., ✨ for features, 🐛 for fixes, ♻️ for refactors).
3. **File Summary**: At the very end of the message, include a section labeled "Total Files Changed:" followed by the count.

## Style Guidelines
- **Be Concise**: Avoid overly detailed explanations or "fluff." Focus on *what* was changed and *why*.
- **Clarity**: Use clear, professional language.
