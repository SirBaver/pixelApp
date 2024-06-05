import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';  // Ajoutez cette ligne

  constructor(private http: HttpClient, private router: Router) { }

  onSubmit(form: NgForm) {
    console.log(form.valid);
    if (form.valid) {
      console.log({ username: this.username, password: this.password });
      this.http.post('http://localhost:5000/register', {username: this.username, password: this.password})
      .subscribe(
        (response) => {
          // Handle successful registration here
        },
        (error) => {
          if (error.status === 400 && error.error === 'Username already exists') {
            // Display the error message
            this.errorMessage = error.error;
          } else {
            // Handle other errors here
          }
        }
      );
    }
  }
}