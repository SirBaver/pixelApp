import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { TranslateModule } from '@ngx-translate/core';

import { RegisterWaitingPageRoutingModule } from './register-waiting-routing.module';
import { RegisterWaitingPage } from './register-waiting.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RegisterWaitingPageRoutingModule,
    TranslateModule.forChild()
  ],
  declarations: [RegisterWaitingPage]
})
export class RegisterWaitingPageModule {}
