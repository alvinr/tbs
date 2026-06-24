// Make every plain markdown table click-sortable (Material instant-loading aware).
document$.subscribe(function () {
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    new Tablesort(table);
  });
});
