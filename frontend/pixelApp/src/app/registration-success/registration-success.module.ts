import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { RegistrationSuccessPageRoutingModule } from './registration-success-routing.module';

import { RegistrationSuccessPage } from './registration-success.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RegistrationSuccessPageRoutingModule
  ],
  declarations: [RegistrationSuccessPage]
})
export class RegistrationSuccessPageModule {}
