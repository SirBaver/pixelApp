import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';

import { PasswordResetPageRoutingModule } from './password-reset-routing.module';
import { PasswordResetPage } from './password-reset.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PasswordResetPageRoutingModule,
    TranslateModule.forChild()
  ],
  declarations: [PasswordResetPage]
})
export class PasswordResetPageModule {}
