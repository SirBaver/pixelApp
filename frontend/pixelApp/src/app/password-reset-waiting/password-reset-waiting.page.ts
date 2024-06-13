import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-password-reset-waiting',
  templateUrl: './password-reset-waiting.page.html',
  styleUrls: ['./password-reset-waiting.page.scss'],
})
export class PasswordResetWaitingPage {
  email: string = ''; // Vous devrez probablement obtenir cet email d'une autre manière, par exemple à partir d'un service partagé.

  constructor(private http: HttpClient, private translate: TranslateService) {}

  resendEmail() {
    this.http.post('http://localhost:5000/auth/reset_password_request', { mail: this.email }).subscribe(
      (response: any) => {
        // Message de succès, si nécessaire
      },
      (error: any) => {
        // Gérer les erreurs, si nécessaire
      }
    );
  }
}
