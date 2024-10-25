ckan.module("latex-parse-form", function ($) {
  "use strict";
  return {
    options: {
      previewPlaceholder: "Preview for the LaTeX input",
      previewIdentifier: "field-latex-preview",
      throwOnError: false,
    },
    initialize: function () {
      this.input = this.el[0]
      this.previewEl = document.querySelector(`#${this.options.previewIdentifier}`);

      if (!this.previewEl) {
        return;
      }
      
      this.input.addEventListener("input", (e) => {
        this.parseTex(e.target.value)

        if (this._isEmpty(this.input)) {
          this.addPlaceholder();
        }
      })

      if (!this._isEmpty(this.input)) {
        this.parseTex(this.input.value);
      } else {
        this.addPlaceholder();
      }
    },
    _isEmpty: function (el) {
      return !el.value ? true : false;
    },
    parseTex: function (v) {
      this.previewEl.innerHTML = v

      renderMathInElement(this.previewEl, {
        delimiters: [{
            left: '$$',
            right: '$$',
            display: true
          },
          {
            left: '$',
            right: '$',
            display: false
          },
          {
            left: '\\(',
            right: '\\)',
            display: false
          },
          {
            left: '\\[',
            right: '\\]',
            display: true
          }
        ],
        throwOnError: this.options.throwOnError
      });
    },
    addPlaceholder: function () {
      this.previewEl.innerHTML = this.options.previewPlaceholder;
    }
  };
});