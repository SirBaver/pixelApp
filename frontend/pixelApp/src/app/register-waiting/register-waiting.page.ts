import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-register-waiting',
  templateUrl: './register-waiting.page.html',
  styleUrls: ['./register-waiting.page.scss'],
})
export class RegisterWaitingPage {
  errorMessage: string = '';

  constructor(private http: HttpClient, private translate: TranslateService) { }

  resendEmail() {
    this.http.post('http://localhost:5000/auth/resend_verification', {}).subscribe(
      (response: any) => {
        // Handle successful resend
        this.translate.get('register.EMAIL_SENT').subscribe((res: string) => {
          alert(res);
        });
      },
      (error: any) => {
        // Handle error
        this.translate.get('register.EMAIL_RESEND_FAILED').subscribe((res: string) => {
          this.errorMessage = res;
        });
      }
    );
  }
}
