import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth-service.service';
import { environment } from '../../environments/environment'; // Importer l'environnement

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private router: Router, private authService: AuthService) { }

  onSubmit(form: NgForm) {
    if (form.valid) {
      this.authService.login(this.username, this.password).subscribe(
        (response: any) => { // Remplacez any par un type plus spécifique si possible
          localStorage.setItem('session_id', response.session_id); // Stocker l'ID de session
          this.router.navigate(['/home']);
        },
        (error: any) => { // Remplacez any par un type plus spécifique si possible
          if (error.status === 400 && error.error === 'Invalid username or password') {
            this.errorMessage = error.error;
          } else {
            // Gestion des autres erreurs ici
            this.errorMessage = 'An unexpected error occurred.';
          }
        }
      );
    }
  }

  navigateToPasswordResetRequest() {
    this.router.navigate(['/login/password-reset-request']);
  }
}
