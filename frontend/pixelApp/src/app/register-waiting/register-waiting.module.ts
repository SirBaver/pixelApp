import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { RegisterWaitingPageRoutingModule } from './register-waiting-routing.module';

import { RegisterWaitingPage } from './register-waiting.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RegisterWaitingPageRoutingModule
  ],
  declarations: [RegisterWaitingPage]
})
export class RegisterWaitingPageModule {}
