import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth-service.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) { }

  onSubmit(form: NgForm) {
    if (form.valid) {
      this.authService.login(this.username, this.password).subscribe(
        (response: any) => { // Remplacez any par un type plus spécifique si possible
          this.router.navigate(['/home']);
        },
        (error: any) => { // Remplacez any par un type plus spécifique si possible
          if (error.status === 400 && error.error === 'Invalid username or password') {
            this.errorMessage = error.error;
          } else {
            // Gestion des autres erreurs ici
          }
        }
      );
    }
  }
}