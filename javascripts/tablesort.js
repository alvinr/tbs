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
// A total / subtotal row is a footer, not data — move it to <tfoot> so tablesort (which only ever
// sorts <tbody> rows) leaves it pinned at the bottom instead of shuffling it into the sort. Detect it
// by CONTENT, not formatting: the BOM total rows have every middle column (Qty/Supplier/Systems) blank;
// the summary/scenario total rows fill every column but are labelled "total" in the first cell.
function isFooterRow(row) {
  var c = row.cells, n = c.length;
  if (!n) return false;
  if (n >= 3) {
    var middleBlank = true;
    for (var i = 1; i < n - 1 && middleBlank; i++) middleBlank = c[i].textContent.trim() === "";
    if (middleBlank) return true;
  }
  return /total/i.test(c[0].textContent);   // "...total" / "...subtotal" / "TOTAL"
}
document$.subscribe(function () {
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    var tbody = table.tBodies[0];
    if (tbody) {
      Array.prototype.slice.call(tbody.rows).forEach(function (row) {
        if (isFooterRow(row)) (table.tFoot || table.createTFoot()).appendChild(row);
      });
    }
    if (!table.dataset.sortInit) { table.dataset.sortInit = "1"; new Tablesort(table); }
  });
});
