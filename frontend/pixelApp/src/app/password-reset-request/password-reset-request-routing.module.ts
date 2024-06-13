import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PasswordResetRequestPage } from './password-reset-request.page';

const routes: Routes = [
  {
    path: '',
    component: PasswordResetRequestPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PasswordResetRequestPageRoutingModule {}
