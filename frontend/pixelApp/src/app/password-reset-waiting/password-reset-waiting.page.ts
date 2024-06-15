import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TranslateService } from '@ngx-translate/core';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-password-reset-waiting',
  templateUrl: './password-reset-waiting.page.html',
  styleUrls: ['./password-reset-waiting.page.scss'],
})
export class PasswordResetWaitingPage {
  errorMessage: string = '';

  constructor(private http: HttpClient, private translate: TranslateService) {}

  resendEmail() {
    const sessionId = localStorage.getItem('session_id');
    if (sessionId) {
      this.http.post(`${environment.apiUrl}/auth/resend_reset`, { session_id: sessionId }).subscribe(
        (response: any) => {
          // Message de succès, si nécessaire
          console.log('Password reset email resent');
        },
        (error: any) => {
          // Gérer les erreurs, si nécessaire
          console.error('Error resending password reset email', error);
          if (error.status === 400) {
            this.translate.get('ERROR_SESSION_INVALID').subscribe((res: string) => {
              this.errorMessage = res;
            });
          } else {
            this.translate.get('ERROR_OCCURRED').subscribe((res: string) => {
              this.errorMessage = res;
            });
          }
        }
      );
    } else {
      this.translate.get('ERROR_SESSION_EXPIRED').subscribe((res: string) => {
        this.errorMessage = res;
      });
    }
  }
}
