// Make every plain markdown table click-sortable (Material instant-loading aware), with
// money-aware numeric sorting so the BOM "Est. cost" / "Qty" columns sort by value, not as text
// (otherwise "$1,170" lands before "$30"). A money/number cell sorts by its first number; a range
// like "$30–$50" sorts by its low value.
if (window.Tablesort) {
  Tablesort.extend("money",
    function (item) { return /^\s*[~$]?\s*-?[\d,]+/.test(item); },
    function (a, b) {
      function num(s) {
        var m = String(s).replace(/,/g, "").match(/-?\d+(\.\d+)?/);
        return m ? parseFloat(m[0]) : 0;
      }
      return num(a) - num(b);
    });
}
document$.subscribe(function () {
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    new Tablesort(table);
  });
});
