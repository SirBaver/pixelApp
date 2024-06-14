import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core'; // Importer TranslateService
import { environment } from '../../environments/environment'; // Importer l'environnement

@Component({
  selector: 'app-password-reset-request',
  templateUrl: './password-reset-request.page.html',
  styleUrls: ['./password-reset-request.page.scss'],
})
export class PasswordResetRequestPage implements OnInit {
  email: string = '';
  errorMessage: string = ''; // Déclarez la propriété errorMessage ici

  constructor(private http: HttpClient, private router: Router, private translate: TranslateService) {
    console.log('PasswordResetRequestPage constructor');
  }

  ngOnInit() {
    console.log('PasswordResetRequestPage ngOnInit');
  }

  onSubmit(form: NgForm) {
    console.log('Request password reset for:', this.email);
    // Ajoutez ici la logique pour appeler votre API de demande de réinitialisation de mot de passe
    if (form.valid) {
      console.log('Form is valid');
      this.http.post(`${environment.apiUrl}/auth/reset_password_request`, { mail: this.email }).subscribe(
        (response: any) => {
          localStorage.setItem('session_id', response.session_id); // Stocker l'ID de session
          this.router.navigate(['/password-reset-waiting']);
        },
        (error: any) => {
          if (error.status === 404) {
            this.translate.get('ERROR_EMAIL_NOT_FOUND').subscribe((res: string) => {
              this.errorMessage = res;
            });
          } else if (error.status === 400) {
            this.translate.get('INVALID_EMAIL_ADDRESS').subscribe((res: string) => {
              this.errorMessage = res;
            });
          } else {
            this.translate.get('ERROR_OCCURRED').subscribe((res: string) => {
              this.errorMessage = res;
            });
          }
        }
      );

      // Pour cet exemple, nous allons juste mettre un message d'erreur simulé
      this.translate.get('ERROR_OCCURRED').subscribe((res: string) => {
        this.errorMessage = res;
      });
    } else {
      this.translate.get('INVALID_EMAIL_ADDRESS').subscribe((res: string) => {
        this.errorMessage = res;
      });
    }
  }
}
