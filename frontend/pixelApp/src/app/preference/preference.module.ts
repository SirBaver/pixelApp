import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { PreferencePageRoutingModule } from './preference-routing.module';

import { PreferencePage } from './preference.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PreferencePageRoutingModule
  ],
  declarations: [PreferencePage]
})
export class PreferencePageModule {}
