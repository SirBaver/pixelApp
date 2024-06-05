import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {
  username: string = '';
  password: string = '';

  constructor(private http: HttpClient) { }

  register() {
    this.http.post('http://localhost:5000/register', {
      username: this.username,
      password: this.password
    }).subscribe(response => {
      console.log(response);
    });
  }
}