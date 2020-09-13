document.getElementById('tabulator-script').addEventListener('load', function () {

  var table = new Tabulator("#serbers", {
    layout:"fitDataFill",
    columns: [
      {title: 'Name'},
      {title: 'Gamemode'},
      {
        title: 'Map', field: 'Map', sorter: 'string', formatter: 'html'
      },
      {title: 'Current Players', field: 'current-players', sorter: 'number', formatter: 'html'},
      {title: 'Max Players', sorter: 'number'},
      {title: 'Location'}
    ],
    initialSort: [{column: 'current-players', dir: 'desc'}]
  });

})
