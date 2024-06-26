import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { environment } from '../../environments/environment'; // Importer l'environnement

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage {
  email: string = '';
  username: string = '';
  password: string = '';
  confirmPassword: string = '';
  language: string = '';
  errorMessage: string = '';

  languages = [
    { code: 'en', label: 'common.ENGLISH' },
    { code: 'fr', label: 'common.FRENCH' },
    { code: 'es', label: 'common.SPANISH' },
  ];

  constructor(private http: HttpClient, private router: Router, private translate: TranslateService) { }

  onSubmit(form: NgForm) {
    if (form.valid) {
      if (this.password !== this.confirmPassword) {
        this.translate.get('register.PASSWORDS_DO_NOT_MATCH').subscribe((res: string) => {
          this.errorMessage = res;
        });
        return;
      }

      const formData = {
        username: this.username,
        password: this.password,
        mail: this.email,
        preferred_language: this.language
      };

      console.log('Form Submitted!', formData);

      this.http.post(`${environment.apiUrl}/auth/register`, formData)
        .subscribe({
          next: (response: any) => {
            console.log('Registration successful', response);
            localStorage.setItem('session_id', response.session_id); // Stocker l'ID de session
            this.router.navigate(['/register/register-waiting']);
            console.log('Redirection vers /register/register-waiting');
          },
          error: (error) => {
            console.error('Registration error', error); // Ajoutez ce log pour voir les détails de l'erreur
            if (error.status === 409 && error.error.message === 'Username already exists') {
              this.translate.get('register.USERNAME_EXISTS').subscribe((res: string) => {
                this.errorMessage = res;
              });
            } else if (error.status === 409 && error.error.message === 'Email already exists') {
              this.translate.get('register.EMAIL_EXISTS').subscribe((res: string) => {
                this.errorMessage = res;
              });
            } else if (error.status === 400 && error.error.message === 'Invalid email format') {
              this.translate.get('register.INVALID_EMAIL_FORMAT').subscribe((res: string) => {
                this.errorMessage = res;
              });
            } else {
              this.translate.get('register.REGISTRATION_FAILED').subscribe((res: string) => {
                this.errorMessage = res;
              });
            }
          },
          complete: () => {
            console.log('Request completed');
          }
        });
    } else {
      this.translate.get('FILL_REQUIRED_FIELDS').subscribe((res: string) => {
        this.errorMessage = res;
      });
    }
  }
}
