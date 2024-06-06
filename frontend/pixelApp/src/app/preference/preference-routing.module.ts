import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PreferencePage } from './preference.page';

const routes: Routes = [
  {
    path: '',
    component: PreferencePage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PreferencePageRoutingModule {}
