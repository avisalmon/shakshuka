import re

with open('c:/Projects/shakshuka/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix selectors
content = content.replace(".vote-btn[data-option]", ".debate-option[data-value]")
content = content.replace("btn.dataset.option", "btn.dataset.value")
content = content.replace("const option = btn.dataset.value;", "const option = btn.dataset.value;")

# Fix applyVoteState bar logic
old_bar = """  // Show vote message
  let msg = card.querySelector('.vote-message');
  if (!msg) {
    msg = document.createElement('div');
    msg.className = 'vote-message';
    msg.style.cssText = 'margin-top:8px;font-size:14px;opacity:.8;';
    const btnContainer = card.querySelector('.vote-buttons') || card.querySelector('.debate-option[data-value]').parentElement;
    if (btnContainer) btnContainer.after(msg);
  }"""

new_bar = """  // Show result bars
  const resultDiv = card.querySelector('.debate-result');
  if (resultDiv) {
    resultDiv.style.display = 'block';
    card.querySelectorAll('.debate-bar-fill[data-option]').forEach(bar => {
      bar.style.transition = 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
      bar.style.width = bar.dataset.option === selectedOption ? '65%' : '35%';
    });
  }

  // Show vote message
  let msg = card.querySelector('.vote-message');
  if (!msg) {
    msg = document.createElement('div');
    msg.className = 'vote-message';
    msg.style.cssText = 'text-align:center;margin-top:12px;font-size:0.9rem;color:var(--olive-green);font-weight:600;';
    const optionsDiv = card.querySelector('.debate-options');
    if (optionsDiv) optionsDiv.after(msg);
  }"""

content = content.replace(old_bar, new_bar)

# Fix the vote bar line
content = content.replace(
    """  // Animate vote bar if exists
  const bar = card.querySelector(`.vote-bar[data-option="${selectedOption}"]`);
  if (bar) {
    bar.style.transition = 'width 0.6s ease';
    bar.style.width = bar.dataset.percent ? bar.dataset.percent + '%' : '100%';
  }""",
    """  const label = card.querySelector(`.debate-option[data-value="${selectedOption}"] .option-label`);"""
)

# Fix vote message text
content = content.replace(
    'msg.textContent = `Your vote: ${selectedOption}`;',
    'msg.textContent = `\\u2713 You voted: ${label ? label.textContent : selectedOption}`;'
)

with open('c:/Projects/shakshuka/js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
