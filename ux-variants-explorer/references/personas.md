# The five test personas

Each persona is defined by needs and context, not demographics. Use the testing goal as the yardstick for that persona's variant.

## 1. The Efficiency Maximalist (power user)

- **Profile:** A professional who spends 10+ hours a day in digital tools. They see software as a utility, not an experience.
- **UX needs:** Keyboard shortcuts, a command palette, dense information displays, bulk actions, and "low-chrome" interfaces. They dislike animations or "delight" features that slow task completion.
- **Typical patterns:** Cmd/Ctrl+K palette, inline editing, multi-select, saved views, and customizable columns.
- **Testing goal:** Does the UI support high-speed navigation and "expert mode" workflows?
- **Signals to measure:** Time on task, keystrokes per task, and mouse-free completion rate.

## 2. The Distracted On-the-Goer (mobile-first)

- **Profile:** A busy parent or field worker using the product in high-stress, low-concentration moments, like standing on a crowded train or holding a shopping bag.
- **UX needs:** Large touch targets (48px+), high-contrast text for outdoor glare, one-handed navigation in the thumb zone, "save for later", and clear interruptibility with automatic draft saving.
- **Typical patterns:** Bottom-anchored primary action, bottom sheets, smart defaults, and resume-where-you-left-off banners.
- **Testing goal:** Can the user complete the core value proposition in under 30 seconds at about 50% of their normal attention?
- **Signals to measure:** Completion time, mis-taps, and resume rate after interruption.

## 3. The Reluctant Adopter (low digital confidence)

- **Profile:** Someone with low digital confidence, often outside tech-heavy work, who worries about "breaking" the software. Modern iconography, like the hamburger menu, is not obvious to them.
- **UX needs:** Explicit text labels instead of icon-only controls, Undo that is more prominent than Delete, confirmation for irreversible actions, and linear step-by-step wizards rather than open dashboards.
- **Typical patterns:** Wizard with a progress bar, plain-language microcopy, inline help, and a summary-before-submit step.
- **Testing goal:** Can users discover the interface without a manual, and does it reassure them enough to prevent errors?
- **Signals to measure:** Unassisted completion rate, error rate, help requests, and self-reported confidence.

## 4. The Accessibility-Dependent (visual impairment)

- **Profile:** A user with low vision or color blindness who relies on a screen reader or extreme browser zoom (200%+).
- **UX needs:** A logical heading structure and landmarks, high color contrast (WCAG AA minimum, AAA preferred), reflow without horizontal scroll at 400% zoom, meaning never carried by color alone, semantic HTML, and clear focus states.
- **Typical patterns:** Skip links, ARIA live regions for status updates, labeled form fields with text errors, and a single-column layout.
- **Testing goal:** Does the UX stay functional and coherent when the visual layout is stripped or heavily distorted?
- **Signals to measure:** Screen-reader task completion, WCAG violations from an automated and manual audit, and reflow breakage.

## 5. The Privacy-Conscious Skeptic (data-leery)

- **Profile:** A user who is highly sensitive to data collection and dark patterns. They abandon a flow if it feels pushy or asks for unnecessary permissions.
- **UX needs:** Transparent "Why we need this" explanations, opt-outs as easy to find as opt-ins, data minimization, and local storage or guest mode instead of forced account creation.
- **Typical patterns:** Guest checkout, just-in-time permission requests, granular consent toggles (none pre-checked), and a visible data summary.
- **Testing goal:** Does the UX build enough trust to convert a skeptical user without coercive design?
- **Signals to measure:** Conversion without an account, permission grant rate, drop-off at data requests, and self-reported trust.
