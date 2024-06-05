import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private http: HttpClient, private router: Router) { }

  onSubmit(form: NgForm) {
    if (form.valid) {
      this.http.post('http://localhost:5000/login', {username: this.username, password: this.password})
      .subscribe(
        (response) => {
          // Handle successful login here, e.g. by navigating to another page
          this.router.navigate(['/home']);
        },
        (error) => {
          if (error.status === 400 && error.error === 'Invalid username or password') {
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