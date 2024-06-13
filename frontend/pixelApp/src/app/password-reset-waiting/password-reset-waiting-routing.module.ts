import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PasswordResetWaitingPage } from './password-reset-waiting.page';

const routes: Routes = [
  {
    path: '',
    component: PasswordResetWaitingPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PasswordResetWaitingPageRoutingModule {}
