import { Component } from '@angular/core';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'scipio';
  
  readTextFile(file){
    // var fileDisplayArea = document.getElementById(elem_name);
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function (){
      if(rawFile.readyState === 4){
        if(rawFile.status === 200 || rawFile.status == 0){
          var allText = rawFile.responseText;
          data=allText;
          // fileDisplayArea.innerText = allText 
        }
      }
    }
    rawFile.send(null);
  }
  
  ngOnInit(){
    this.readTextFile("../assets/scipio_title.txt");
    var header = document.getElementById('title');
    header.innerHTML=data;

    this.start_listener();

    this.set_graphs();


    // this.update_graphs();
  }

  start_listener(){
    var elem=document.getElementById('stop-button');
    // elem.addEventListener('click',function(){executing=false});
  }

  // update_graphs(){
  //   do{
  //     // this.set_graphs();
  //     console.log('hi');
  //   }
  //   while (executing==true);

  // }
  
  set_graphs(){   
    this.readTextFile('../assets/example_arch.txt');
    var arch_types=['avr', 'alphaev56', 'arm', 'm68k', 'mips', 'mipsel', 'powerpc', 's390', 'sh4', 'sparc', 'x86_64', 'xtensa'];
    var chart=document.getElementById('chart-arch');
    var chart_arch_data= [{
      label: 'Architecture Slice Types',
      backgroundColor: '#0f0f0f',
      borderColor: '#bf00ff',
      borderWidth:1,
      data: data.split(',')
    }]
    this.create_chart(chart,'bar',arch_types,chart_arch_data,true);
    
    this.readTextFile('../assets/example_acc.txt');
    var chart=document.getElementById('chart-acc');
    var chart_line_data= [{
      label: 'AI Guess Accuracy',
      borderColor: '#bf00ff',
      fill:false,
      borderWidth:1,
      data: data.split(',')
    }]
    this.create_chart(chart,'line',["","","","","","","","","","","",""],chart_line_data,false);
    
    this.readTextFile('../assets/example_dough.txt');
    var chart=document.getElementById('chart-dough');
    var chart_dough_data= [{
      label: 'Planets Discovered by Kepler',
      backgroundColor: [],
      borderColor: ['#bf00ff','#bf00ff','#bf00ff'],
      borderWidth:1,
      data: data.split(',')
    }]
    this.create_chart(chart,'doughnut',["thing","thing","thing"],chart_dough_data,true);
    
    this.readTextFile('../assets/example_conf.txt');
    var chart=document.getElementById('chart-conf');
    var chart_conf_data= [{
      label: 'AI Answer Confidence',
      backgroundColor: '#0f0f0f',
      borderColor: '#bf00ff',
      borderWidth:1,
      data: data.split(',')
    }]
    this.create_chart(chart,'bar',[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],chart_conf_data,true);
    
    return;
  }
  
  create_chart(chart_element,chart_type,chart_labels,chart_data,zero){
    var new_chart = new Chart(chart_element, {
      type: chart_type,
      data: {
        labels: chart_labels,
        datasets: chart_data,
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: zero
            }
          }]
        }
      }
    });
  }
  
}

var data;
// var executing=true;

