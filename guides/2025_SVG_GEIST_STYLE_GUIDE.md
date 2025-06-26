A complete SVG iconography style guide is essential for any modern design system, especially at scale, because it ensures consistency, clarity, and efficiency across all digital products. Below is a meticulous and comprehensive SVG icon style guide, integrating best practices from industry sources and explicitly reflecting the Geist and Vercel v0 design philosophies[1][2][5][6].

---

## SVG Iconography Style Guide

### **1. Purpose & Philosophy**

- **Consistency:**  
  Icons are visual language. Consistent style, scale, and alignment are crucial for a polished, professional interface[1][2].
- **Simplicity & Clarity:**  
  Icons must be immediately recognizable, using minimal details and universally understood symbols[5].
- **Scalability:**  
  SVGs are vector-based and must remain crisp at all sizes, from small buttons to large hero graphics[5][6].
- **Brand Alignment:**  
  Icon style should reflect your brand’s voice—in this case, minimalist, geometric, and precise, as inspired by Geist and Vercel v0.

---

### **2. Artboard & Grid**

- **Canvas Size:**  
  All icons are designed on a 24x24 pixel grid[6].
- **Pixel Grid Alignment:**  
  Anchor strokes and shapes to the pixel grid to avoid blurriness at small sizes[1].
- **Padding:**  
  Maintain even internal padding; no strokes should touch the artboard’s edge.

---

### **3. Style & Construction**

- **Stroke vs. Fill:**  
  Use a line-based (stroked) style for all icons. Only use fills for accent or selection states, and never mix filled and outlined icons in the same set[2][7].
- **Stroke Weight:**  
  Default stroke width is 2px. All icons in the set must use this weight for visual harmony[2][5].
- **Stroke Attributes:**  
  - `stroke-linecap="round"`
  - `stroke-linejoin="round"`
  - `stroke="currentColor"` (enables theming via CSS)
- **Corner Radius:**  
  Use rounded corners and endpoints for a modern, approachable look.

---

### **4. Color & Theming**

- **Primary Color:**  
  Icons inherit color from their parent context using `currentColor`. This supports light/dark themes and dynamic color changes[1][4].
- **Accent Colors:**  
  Use accent colors sparingly and only for interactive or selected states.
- **No Gradients or Shadows:**  
  Keep icon colors flat and simple for clarity and scalability.

---

### **5. Sizing & Spacing**

- **Standard Sizes:**  
  Use 24px as the default. If additional sizes are needed, stick to the 4px grid (16, 20, 24, 28, 32, etc.)[6].
- **Spacing:**  
  Ensure internal elements have at least the stroke width (2px) of space between them[2].
- **Alignment:**  
  Center icons visually within the 24x24 grid.

---

### **6. Accessibility**

- **ARIA Attributes:**  
  - Add `role="img"` to every SVG.
  - Use `aria-label="Description"` for meaningful icons.
  - For decorative icons, use `aria-hidden="true"`[4][5].
- **Contrast:**  
  Ensure icons meet WCAG AA contrast standards when used as interactive elements.

---

### **7. File Structure & Export**

- **SVG Export:**  
  - Remove unnecessary metadata, comments, and hidden layers.
  - Use presentation attributes (`stroke`, `fill`, etc.) rather than inline styles for easier theming[1].
  - Name layers and IDs meaningfully for maintainability[1].
- **CSS Control:**  
  - Prefer SVGs with `currentColor` for stroke/fill to enable dynamic color via CSS[1][3].
- **React Integration:**  
  - Use SVGR or similar tools to convert SVGs into React components, passing `className`, `aria-label`, and other props as needed.

---

### **8. Usage Patterns**

- **Inline SVG:**  
  - Place SVG markup directly in the HTML or JSX for full styling and accessibility control[3][4].
- **Symbol Sprites:**  
  - For large icon sets, use `` and `` for efficient referencing and reduced markup[3].
- **CSS Pseudo-elements:**  
  - Use only for decorative icons where accessibility is not required[3].

---

### **9. Examples**

**Basic SVG Icon:**
```xml

  
  

```

---

### **10. Do’s and Don’ts**

**Do:**
- Use a consistent 2px stroke for all icons[2][5].
- Align all icons to a 24x24 grid[6].
- Use `currentColor` for dynamic theming[1].
- Keep icons simple and recognizable[5].
- Provide ARIA labels for accessibility[4][5].

**Don’t:**
- Mix filled and outlined icons in the same set[2].
- Use multiple stroke weights within a set[2][5].
- Add unnecessary visual detail or color.
- Allow strokes to touch the artboard edge.
- Use color as the only way to convey meaning.

---

### **11. Review & Maintenance**

- **Approval:**  
  All new icons must be reviewed for consistency with the style guide before being added to the library[1].
- **Documentation:**  
  Maintain a visual reference of all approved icons, including usage notes and accessibility guidance[1][2].

---

**Summary:**  
This meticulous style guide ensures your SVG iconography is consistent, accessible, scalable, and aligned with modern UI/UX and brand principles—minimizing rework and maximizing clarity and professionalism across your product suite[1][2][5][6].

[1] https://www.creativefreedom.co.uk/icon-designers-blog/svg-icons-for-ui-and-software-designers-myths-and-best-practices/
[2] https://www.designsystems.com/iconography-guide/
[3] https://chenhuijing.com/blog/the-many-methods-for-using-svg-icons/
[4] https://design-system.w3.org/styles/svg-icons.html
[5] https://blog.pixelfreestudio.com/best-practices-for-using-icons-and-illustrations-in-design-systems/
[6] https://www.koalaui.com/blog/ultimate-guide-best-practices-icons-2024
[7] https://blog.thenounproject.com/a-completely-awesome-guide-to-icon-styles-and-file-formats/
[8] https://stackoverflow.com/questions/9647770/what-are-best-practices-for-using-svg-icons-on-android