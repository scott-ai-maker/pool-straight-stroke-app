# Contributing to Pool Stroke Trainer

Thank you for your interest in contributing to Pool Stroke Trainer! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background, experience level, gender identity, sexual orientation, disability, personal appearance, race, ethnicity, age, religion, or nationality.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of Flask, OpenCV, and web development
- Familiarity with computer vision concepts (helpful but not required)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pool-straight-stroke-app.git
   cd pool-straight-stroke-app
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/scott-ai-maker/pool-straight-stroke-app.git
   ```

## 💻 Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Development Tools

```bash
pip install flake8 black pylint mypy pytest
```

### 4. Run Application

```bash
python app.py
```

Visit `http://localhost:7860` to verify setup.

## 🎨 How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes** - Fix issues or improve error handling
2. **Features** - Add new functionality or enhance existing features
3. **Documentation** - Improve docs, add examples, fix typos
4. **Performance** - Optimize code for speed or efficiency
5. **Testing** - Add or improve test coverage
6. **UI/UX** - Enhance user interface or experience

### Contribution Workflow

1. **Check Existing Issues** - Look for existing issues or create a new one
2. **Discuss** - Comment on the issue to discuss your approach
3. **Create Branch** - Create a feature branch from `main`
4. **Develop** - Make your changes following coding standards
5. **Test** - Ensure your changes work and don't break existing functionality
6. **Commit** - Write clear, descriptive commit messages
7. **Push** - Push your changes to your fork
8. **Pull Request** - Submit a PR with detailed description

### Branch Naming

Use descriptive branch names:
- `feature/add-blue-marker-detection`
- `bugfix/camera-permission-error`
- `docs/update-installation-guide`
- `refactor/improve-analyzer-performance`

## 📝 Coding Standards

### Python Style Guide

Follow **PEP 8** style guide:

```python
# Good: Clear, descriptive names with proper spacing
def calculate_stroke_metrics(points: List[Tuple[int, int]]) -> Optional[StrokeMetrics]:
    """Calculate comprehensive stroke quality metrics.
    
    Args:
        points: List of (x, y) coordinate tuples.
        
    Returns:
        StrokeMetrics object or None if insufficient data.
    """
    if len(points) < 5:
        return None
    # ... implementation
```

**Key Points:**
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter default)
- Use type hints for function parameters and return values
- Write docstrings for all functions, classes, and modules
- Use descriptive variable names

### JavaScript Style Guide

Follow **ES6+ standards**:

```javascript
// Good: Clear async/await with proper error handling
async function processFrame(imageData, isTracking) {
    try {
        const response = await fetch('/api/process_frame', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData, tracking: isTracking })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Frame processing error:', error);
        throw error;
    }
}
```

**Key Points:**
- Use `const` and `let`, avoid `var`
- Use arrow functions where appropriate
- Prefer async/await over callbacks
- Add JSDoc comments for functions
- Use meaningful variable names

### CSS Style Guide

Follow **BEM methodology**:

```css
/* Good: BEM naming with clear hierarchy */
.metrics-panel {
    background: var(--bg-secondary);
    border-radius: var(--border-radius);
}

.metrics-panel__header {
    color: var(--primary-color);
}

.metrics-panel__item--highlighted {
    font-weight: 700;
}
```

**Key Points:**
- Use CSS custom properties for theming
- Mobile-first responsive design
- Meaningful class names
- Group related styles together

### Documentation

- Use clear, concise language
- Include code examples
- Update README.md for new features
- Add inline comments for complex logic
- Keep API.md synchronized with code

## 🧪 Testing Guidelines

### Running Tests

```bash
# Python linting
flake8 app.py stroke_analyzer.py

# Type checking
mypy app.py stroke_analyzer.py

# Code formatting (auto-fix)
black app.py stroke_analyzer.py

# Manual testing
python app.py
# Test in browser at http://localhost:7860
```

### Test Checklist

Before submitting a PR, verify:

- [ ] Code follows style guidelines (flake8 passes)
- [ ] Type hints are correct (mypy passes)
- [ ] Code is formatted (black applied)
- [ ] Application starts without errors
- [ ] Camera access works in browser
- [ ] Frame processing works correctly
- [ ] Metrics display accurately
- [ ] Reset functionality works
- [ ] Mobile responsive design maintained
- [ ] No console errors in browser
- [ ] Documentation updated if needed

### Writing Tests

When adding tests (future enhancement):

```python
import pytest
from stroke_analyzer import PoolStrokeAnalyzer

def test_analyzer_initialization():
    """Test analyzer initializes with correct parameters."""
    analyzer = PoolStrokeAnalyzer(max_points=20, deviation_threshold=10.0)
    assert analyzer.max_points == 20
    assert analyzer.deviation_threshold == 10.0

def test_invalid_parameters_raise_error():
    """Test that invalid parameters raise ValueError."""
    with pytest.raises(ValueError):
        PoolStrokeAnalyzer(max_points=200)  # Exceeds maximum
```

## 📤 Pull Request Process

### Before Submitting

1. **Sync with upstream:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all checks:**
   ```bash
   flake8 app.py stroke_analyzer.py
   black app.py stroke_analyzer.py
   mypy app.py stroke_analyzer.py
   ```

3. **Test thoroughly** - Verify all functionality works

### PR Description Template

Use this template for your PR:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe testing performed:
- [ ] Manual testing on desktop
- [ ] Manual testing on mobile
- [ ] All checks passing

## Screenshots
If applicable, add screenshots.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Mobile responsive
```

### Review Process

1. **Automated Checks** - Must pass (when CI/CD implemented)
2. **Code Review** - Maintainer reviews changes
3. **Feedback** - Address review comments
4. **Approval** - Maintainer approves PR
5. **Merge** - PR merged to main branch

### After Merge

- Your contribution will be acknowledged in CHANGELOG.md
- Feature will be included in next release
- You'll be added to contributors list (if desired)

## 🐛 Reporting Issues

### Before Reporting

1. **Search existing issues** - Your issue may already be reported
2. **Try latest version** - Issue may be fixed in latest code
3. **Gather information** - Collect relevant details

### Issue Template

```markdown
## Description
Clear description of the issue.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 22.04]
- Browser: [e.g., Chrome 120, Firefox 121]
- Python Version: [e.g., 3.10.8]
- Application Version: [e.g., 1.0.0]

## Screenshots
If applicable, add screenshots.

## Additional Context
Any other relevant information.
```

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `performance` - Performance improvement
- `question` - Further information requested

## 💡 Feature Requests

We welcome feature suggestions! Use this template:

```markdown
## Feature Description
Clear description of the proposed feature.

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How would you implement this feature?

## Alternatives Considered
What other solutions have you considered?

## Additional Context
Any other relevant information, mockups, or examples.
```

### Feature Evaluation Criteria

Features are evaluated based on:
- **Alignment** - Fits project goals and scope
- **Impact** - Benefits many users
- **Feasibility** - Technically achievable
- **Maintenance** - Sustainable long-term
- **Complexity** - Reasonable implementation effort

## 🏆 Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- README.md contributors section (optional)
- GitHub contributors graph

## 📞 Contact

Questions about contributing?
- 📧 Email: scott.aiengineer@outlook.com
- 🐙 GitHub Issues: [Ask a Question](https://github.com/scott-ai-maker/pool-straight-stroke-app/issues)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [PEP 8 Style Guide](https://pep8.org/)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)

---

Thank you for contributing to Pool Stroke Trainer! 🎱
