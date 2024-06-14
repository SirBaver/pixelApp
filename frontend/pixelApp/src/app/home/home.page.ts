import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  data: any;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getData().subscribe(response => {
      this.data = response;
      console.log(this.data);
    });
  }
}
