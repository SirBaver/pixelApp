import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';

import { PasswordResetWaitingPageRoutingModule } from './password-reset-waiting-routing.module';
import { PasswordResetWaitingPage } from './password-reset-waiting.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PasswordResetWaitingPageRoutingModule,
    TranslateModule.forChild()  // Assurez-vous que TranslateModule est importé ici
  ],
  declarations: [PasswordResetWaitingPage]
})
export class PasswordResetWaitingPageModule {}
