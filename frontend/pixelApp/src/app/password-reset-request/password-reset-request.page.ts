import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { TranslateService } from '@ngx-translate/core'; // Importer TranslateService

@Component({
  selector: 'app-password-reset-request',
  templateUrl: './password-reset-request.page.html',
  styleUrls: ['./password-reset-request.page.scss'],
})
export class PasswordResetRequestPage implements OnInit {
  email: string = '';
  errorMessage: string = ''; // Déclarez la propriété errorMessage ici

  constructor(private translate: TranslateService) { // Injecter TranslateService
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
      // Simulation d'une demande de réinitialisation
      // Remplacez cette partie par un appel réel à votre API
      // Exemple:
      // this.http.post('API_URL', { email: this.email }).subscribe(
      //   response => {
      //     // Gérer la réponse positive
      //   },
      //   error => {
      //     this.translate.get('ERROR_OCCURRED').subscribe((res: string) => {
      //       this.errorMessage = res;
      //     });
      //   }
      // );

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
