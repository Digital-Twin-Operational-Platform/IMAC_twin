function myFunc(graph){
    var tester = document.getElementById('geom');
    Plotly.newPlot(tester, graph, {displaylogo : false});

    // Can set cookie in flask redirect and use it here to open a navtab on reload. By style.display = block
    // const vl = document.cookie;  

    // function to click and get data
    tester.on('plotly_click', function(graph){
        var name = graph.points.map(function(d){
            return (d.data.name+ '/' + d.x + '/' + d.y + '/' + d.z);
            // //   for other details use something like => d.data.name+': x= '+d.x+', y= '+d.y
        });
        document.getElementById('SnsrDatum').value = name

    })
}

// Display on click - Sensor Nav
function ssropen(id){
    const frm = document.getElementById('frm1');
    const frm2 = document.getElementById('frm3');
    const frm3 = document.getElementById('frm2');
    const plt = document.getElementById('geom');
    if(frm.style.display === 'none'){
        frm.style.display = 'block';
        // Closes other nav tabs if open
        frm2.style.display = 'none';
        frm3.style.display = 'none';
        plt.style.marginTop = '-18%';
    }
    else{
        frm.style.display = 'none';
        plt.style.marginTop = '-3%' ;
    }
    
}

// Display on click - Mesh Nav
function mshopen(id){
    const frm = document.getElementById('frm2');
    const frm2 = document.getElementById('frm3');
    const frm3 = document.getElementById('frm1');
    const plt = document.getElementById('geom');
    if(frm.style.display === 'none'){
        frm.style.display = 'block';
        frm2.style.display = 'none';
        frm3.style.display = 'none';
        plt.style.marginTop = '-18%';
    }
    else{
        frm.style.display = 'none';
        plt.style.marginTop = '-3%' ;
    }
    
}

// Display on click - KG-querry Nav
function kgqopen(id){
    const frm = document.getElementById('frm3');
    const frm2 = document.getElementById('frm2');
    const frm3 = document.getElementById('frm1');
    const plt = document.getElementById('geom');
    if(frm.style.display === 'none'){
        frm.style.display = 'block';
        frm2.style.display = 'none';
        frm3.style.display = 'none';
        plt.style.marginTop = '-18%';
    }
    else{
        frm.style.display = 'none';
        plt.style.marginTop = '-3%' ;
    }
    
}

// var graphs = {{graphJSON | safe}};
// Plotly.newPlot('chart',graphs,{displaylogo : false}); 

// var tester = document.getElementById('chart');
// tester.on('plotly_click', function(graphs){ 
// // return statement
// var xaxs = graphs.points.map(function(d){
//   return (d.data.name);
// //   for ather details use something like => d.data.name+': x= '+d.x+', y= '+d.y
// });     
// alert('Enter the mesh size for : '+xaxs)
// })