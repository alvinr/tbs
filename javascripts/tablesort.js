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
// System deep-link filter: a `?system=<name>` query param (how a report's parts section links into
// the Master Shopping List) shows only the BOM rows whose "Systems" column contains that system, and
// collapses the type sections it empties — so the reader lands on just that system's slice of the
// by-type BOM. "Show all" drops the param. Tables without a Systems column (summary, suppliers) are
// left untouched. Runs on every instant-loading navigation, so it also RESTORES on a param-less page.
function sysTokens(s) { return s.toLowerCase().split(/[^a-z0-9-]+/).filter(Boolean); }
function applySystemFilter() {
  var sys = (new URLSearchParams(location.search).get("system") || "").trim().toLowerCase();
  var old = document.getElementById("system-filter-banner");
  if (old) old.remove();
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    var head = table.tHead && table.tHead.rows[0], tbody = table.tBodies[0], sysCol = -1;
    if (head) Array.prototype.forEach.call(head.cells, function (c, i) {
      if (c.textContent.trim().toLowerCase() === "systems") sysCol = i;
    });
    if (sysCol < 0 || !tbody) return;   // not a by-system BOM table — leave it alone
    var shown = 0;
    Array.prototype.forEach.call(tbody.rows, function (row) {
      var cell = row.cells[sysCol];
      var show = !sys || (cell && sysTokens(cell.textContent).indexOf(sys) >= 0);
      row.style.display = show ? "" : "none";
      if (show) shown++;
    });
    var collapse = !!sys && shown === 0;
    table.style.display = collapse ? "none" : "";
    var heading = table.previousElementSibling;   // the ### type heading for this section
    if (heading && /^H[1-6]$/.test(heading.tagName)) heading.style.display = collapse ? "none" : "";
  });
  if (sys) {
    var banner = document.createElement("div");
    banner.id = "system-filter-banner";
    banner.style.cssText = "margin:0 0 1rem;padding:.5rem .75rem;border-left:4px solid var(--md-accent-fg-color,#2960A0);" +
      "background:var(--md-code-bg-color,#f5f5f5);border-radius:.1rem;font-size:.8rem;";
    banner.innerHTML = "Filtered to <strong>" + sys.replace(/[^a-z0-9-]/g, "") +
      "</strong> items only. <a href=\"" + location.pathname + "\">Show all →</a>";
    var article = document.querySelector("article");
    if (article) article.insertBefore(banner, article.firstChild);
  }
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
  applySystemFilter();
});
