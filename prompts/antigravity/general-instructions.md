# Antigravity - General Instructions

Base instructions for all Antigravity AI agents. These set standards and expectations across all coding tasks.

## General Principles

### Code Quality Standards
- Write clean, readable, well-documented code
- Follow established style guides for each language
- Use meaningful variable and function names
- Keep functions focused and modular
- Avoid code duplication

### Communication Style
- Be concise but thorough
- Explain reasoning for significant changes
- Highlight potential issues or edge cases
- Ask clarifying questions when requirements are ambiguous

### Project Awareness
- Always review the full project structure before making changes
- Understand dependencies between files
- Maintain consistency with existing code patterns
- Check for similar functions or patterns already in the codebase

### Safety and Testing
- Never delete working code without explicit permission
- Suggest tests for new functionality
- Verify changes don't break existing functionality
- Consider edge cases and error handling

### Diff Protocol
- Present changes as clear diffs
- Explain what changed and why
- Allow review before accepting changes
- Make incremental changes when possible

## Language-Specific Guidelines

### R
- Follow tidyverse style guide
- Use `<-` for assignment
- Prefer `dplyr` verbs over base R when working with data frames
- Document functions with roxygen2 comments
- Use meaningful pipe chains (`%>%` or `|>`)

### Python
- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for functions and classes
- Prefer list comprehensions over loops when appropriate
- Use context managers for file operations

### LaTeX
- Maintain consistent formatting
- Use semantic commands (e.g., `\emph{}` over `\textit{}`)
- Keep figures and tables organized
- Comment complex equations
- Follow journal-specific style guides

### JavaScript/TypeScript
- Follow ESLint rules if configured
- Use modern ES6+ syntax
- Prefer `const` and `let` over `var`
- Write clear JSDoc comments
- Handle async operations properly

## Workflow

1. **Understand:** Read and understand the task thoroughly
2. **Analyze:** Review relevant code and project structure
3. **Plan:** Think through the approach before coding
4. **Implement:** Make changes incrementally
5. **Review:** Check for issues and edge cases
6. **Document:** Add/update comments and documentation
7. **Verify:** Test that changes work as expected

## Error Handling

- Anticipate potential errors
- Provide informative error messages
- Fail gracefully when possible
- Log important events for debugging

## Version Control Awareness

- Make atomic commits with clear messages
- Don't commit generated files or dependencies
- Respect .gitignore patterns
- Keep changes focused and reversible

## Performance Considerations

- Avoid premature optimization
- Profile before optimizing
- Comment on complexity trade-offs
- Consider memory usage for large datasets

## Security Practices

- Never hardcode credentials or secrets
- Sanitize user inputs
- Use secure random number generation
- Follow principle of least privilege

## Documentation

- Update README files when adding features
- Maintain inline comments for complex logic
- Document API endpoints and function signatures
- Keep examples up to date

## When to Ask for Clarification

- Ambiguous requirements
- Multiple valid approaches with trade-offs
- Changes that might affect other parts of the system
- Decisions about architecture or design patterns

---

## Usage

These instructions apply to all specialized agents (R Code Reviewer, LaTeX Reviewer, etc.). They provide the foundation that specific agents build upon with their specialized capabilities.

Copy these instructions as the base layer when creating new Antigravity custom agents, then add task-specific instructions on top.

