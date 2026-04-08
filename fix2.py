with open('c:/Projects/shakshuka/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    if (optionsDiv) optionsDiv.after(msg);
  }
  msg.textContent = `\\u2713 You voted: ${label ? label.textContent : selectedOption}`;

  const label = card.querySelector(`.debate-option[data-value="${selectedOption}"] .option-label`);
}'''

new = '''    if (optionsDiv) optionsDiv.after(msg);
  }
  const label = card.querySelector(`.debate-option[data-value="${selectedOption}"] .option-label`);
  msg.textContent = `\\u2713 You voted: ${label ? label.textContent : selectedOption}`;
}'''

if old in content:
    content = content.replace(old, new)
    with open('c:/Projects/shakshuka/js/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed label order")
else:
    print("Pattern not found")
