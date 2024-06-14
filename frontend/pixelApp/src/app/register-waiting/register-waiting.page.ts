import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TranslateService } from '@ngx-translate/core';
import { environment } from '../../environments/environment'; // Importer l'environnement

@Component({
  selector: 'app-register-waiting',
  templateUrl: './register-waiting.page.html',
  styleUrls: ['./register-waiting.page.scss'],
})
export class RegisterWaitingPage {
  errorMessage: string = '';

  constructor(private http: HttpClient, private translate: TranslateService) { }

  resendEmail() {
    const sessionId = localStorage.getItem('session_id');
    if (sessionId) {
      this.http.post(`${environment.apiUrl}/auth/resend_verification`, { session_id: sessionId }).subscribe(
        (response: any) => {
          // Handle successful resend
          this.translate.get('register.EMAIL_SENT').subscribe((res: string) => {
            alert(res);
          });
        },
        (error: any) => {
          // Handle error
          console.error('Error resending verification email', error);
          if (error.status === 400) {
            this.translate.get('ERROR_SESSION_INVALID').subscribe((res: string) => {
              this.errorMessage = res;
            });
          } else {
            this.translate.get('register.EMAIL_RESEND_FAILED').subscribe((res: string) => {
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
