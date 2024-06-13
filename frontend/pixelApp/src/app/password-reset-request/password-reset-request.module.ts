import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';


import { PasswordResetRequestPageRoutingModule } from './password-reset-request-routing.module';

import { PasswordResetRequestPage } from './password-reset-request.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PasswordResetRequestPageRoutingModule,
    TranslateModule.forChild()
  ],
  declarations: [PasswordResetRequestPage]
})
export class PasswordResetRequestPageModule {}
