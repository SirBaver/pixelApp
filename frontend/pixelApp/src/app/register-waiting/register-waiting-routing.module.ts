import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RegisterWaitingPage } from './register-waiting.page';

const routes: Routes = [
  {
    path: '',
    component: RegisterWaitingPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class RegisterWaitingPageRoutingModule {}
