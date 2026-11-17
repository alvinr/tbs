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
// System filter: a `?system=<a>,<b>,…` query param (how a report's parts section deep-links in, and
// what the on-page chip bar reads/writes) shows only the BOM rows whose "Systems" column names ANY of
// the selected systems (OR), collapsing the type sections it empties. The chip bar is built from the
// systems actually present in the tables (no hardcoded list), so it never drifts; toggling a chip
// rewrites the param via replaceState (no reload, still shareable) and re-applies. Tables without a
// Systems column (summary, suppliers) are left untouched. Runs on every instant-loading navigation.
function sysTokens(s) { return s.toLowerCase().split(/[^a-z0-9-]+/).filter(Boolean); }
function activeSystems() { return sysTokens(new URLSearchParams(location.search).get("system") || ""); }
function bomSysCol(table) {   // index of the "Systems" column, or -1 if this isn't a by-system BOM table
  var head = table.tHead && table.tHead.rows[0];
  if (!head || !table.tBodies[0]) return -1;
  for (var i = 0; i < head.cells.length; i++)
    if (head.cells[i].textContent.trim().toLowerCase() === "systems") return i;
  return -1;
}
function setSystems(list) {
  history.replaceState(null, "", location.pathname + (list.length ? "?system=" + list.join(",") : ""));
  applySystemFilter();
}
function applySystemFilter() {
  var active = activeSystems(), set = {};
  active.forEach(function (s) { set[s] = 1; });
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    var sysCol = bomSysCol(table);
    if (sysCol < 0) return;   // not a by-system BOM table — leave it alone
    var shown = 0;
    Array.prototype.forEach.call(table.tBodies[0].rows, function (row) {
      var cell = row.cells[sysCol];
      var show = !active.length || (cell && sysTokens(cell.textContent).some(function (t) { return set[t]; }));
      row.style.display = show ? "" : "none";
      if (show) shown++;
    });
    var collapse = active.length > 0 && shown === 0;
    var block = table.closest(".md-typeset__scrollwrap") || table;   // Material wraps each data table at runtime; hide the wrapper so no empty margin box is left
    block.style.display = collapse ? "none" : "";
    var heading = block.previousElementSibling;   // the ### type heading for this section
    if (heading && /^H[1-6]$/.test(heading.tagName)) heading.style.display = collapse ? "none" : "";
  });
  buildFilterBar(active);
}
function buildFilterBar(active) {
  var old = document.getElementById("system-filter-bar");
  if (old) old.remove();
  var found = {}, firstTable = null;
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    var sysCol = bomSysCol(table);
    if (sysCol < 0) return;
    if (!firstTable) firstTable = table;
    Array.prototype.forEach.call(table.tBodies[0].rows, function (row) {
      var cell = row.cells[sysCol];
      if (cell) sysTokens(cell.textContent).forEach(function (t) { found[t] = 1; });
    });
  });
  var systems = Object.keys(found).sort();
  if (!systems.length || !firstTable) return;
  var set = {};
  active.forEach(function (s) { set[s] = 1; });
  var bar = document.createElement("div");
  bar.id = "system-filter-bar";
  bar.style.cssText = "margin:0 0 1rem;padding:.6rem .75rem;border-left:4px solid var(--md-accent-fg-color,#2960A0);" +
    "background:var(--md-code-bg-color,#f5f5f5);border-radius:.1rem;font-size:.8rem;display:flex;flex-wrap:wrap;gap:.35rem;align-items:center;";
  var label = document.createElement("span");
  label.textContent = "Filter by system:";
  label.style.cssText = "font-weight:600;margin-right:.25rem;";
  bar.appendChild(label);
  systems.forEach(function (s) {
    var on = !!set[s];
    var chip = document.createElement("button");
    chip.type = "button";
    chip.textContent = s;
    chip.setAttribute("aria-pressed", on ? "true" : "false");
    chip.style.cssText = "cursor:pointer;border-radius:1rem;padding:.15rem .6rem;font-size:.75rem;line-height:1.4;" +
      "border:1px solid var(--md-accent-fg-color,#2960A0);" +
      (on ? "background:var(--md-accent-fg-color,#2960A0);color:#fff;" : "background:transparent;color:var(--md-accent-fg-color,#2960A0);");
    chip.addEventListener("click", function () {
      var next = activeSystems().filter(function (x) { return x !== s; });
      if (!on) next.push(s);
      setSystems(next);
    });
    bar.appendChild(chip);
  });
  if (active.length) {
    var clear = document.createElement("button");
    clear.type = "button";
    clear.textContent = "Show all";
    clear.style.cssText = "cursor:pointer;margin-left:.25rem;border:none;background:none;text-decoration:underline;" +
      "color:var(--md-accent-fg-color,#2960A0);font-size:.75rem;";
    clear.addEventListener("click", function () { setSystems([]); });
    bar.appendChild(clear);
  }
  var block = firstTable.closest(".md-typeset__scrollwrap") || firstTable;
  var heading = block.previousElementSibling;
  var anchor = (heading && /^H[1-6]$/.test(heading.tagName)) ? heading : block;   // sit just above the first type section
  anchor.parentNode.insertBefore(bar, anchor);
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
