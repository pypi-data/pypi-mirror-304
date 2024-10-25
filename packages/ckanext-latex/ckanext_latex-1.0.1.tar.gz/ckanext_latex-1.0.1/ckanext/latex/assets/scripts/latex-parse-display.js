ckan.module("latex-parse-display", function ($) {
  "use strict";
  return {
    options: {},
    initialize: function () {
      var el = this.el[0];
      $(document).ready(function () {
        renderMathInElement(el, {
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
          throwOnError: false
        });
      });
    },
  };
});