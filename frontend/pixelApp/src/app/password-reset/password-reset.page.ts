import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.page.html',
  styleUrls: ['./password-reset.page.scss'],
})
export class PasswordResetPage {
  newPassword: string = '';
  confirmPassword: string = '';
  errorMessage: string = '';
  token: string = '';

  constructor(
    private http: HttpClient, 
    private route: ActivatedRoute, 
    private router: Router, 
    private translate: TranslateService
  ) {
    this.route.queryParams.subscribe(params => {
      this.token = params['token'];
    });
  }

  onSubmit(form: NgForm) {
    if (form.valid) {
      if (this.newPassword !== this.confirmPassword) {
        this.translate.get('password_reset.PASSWORDS_DO_NOT_MATCH').subscribe((res: string) => {
          this.errorMessage = res;
        });
        return;
      }

      this.http.post('http://localhost:5000/auth/reset_password', { token: this.token, new_password: this.newPassword }).subscribe(
        (response: any) => {
          this.router.navigate(['/home']);
        },
        (error: any) => {
          if (error.status === 400 && error.error.message === 'The token is invalid or has expired.') {
            this.translate.get('password_reset.INVALID_TOKEN').subscribe((res: string) => {
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
      this.translate.get('FILL_REQUIRED_FIELDS').subscribe((res: string) => {
        this.errorMessage = res;
      });
    }
  }
}
