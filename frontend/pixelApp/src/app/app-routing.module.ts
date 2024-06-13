import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {path: 'home', loadChildren: () => import('./home/home.module').then( m => m.HomePageModule)},
  {path: 'login', loadChildren: () => import('./login/login.module').then(m => m.LoginPageModule) },
  {path: 'register', loadChildren: () => import('./register/register.module').then(m => m.RegisterPageModule) },
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: 'preference', loadChildren: () => import('./preference/preference.module').then( m => m.PreferencePageModule)},
  {path: 'main', loadChildren: () => import('./main/main.module').then( m => m.MainPageModule)},
  {path: 'profile', loadChildren: () => import('./profile/profile.module').then( m => m.ProfilePageModule)},
  {
    path: 'password-reset-request',
    loadChildren: () => import('./password-reset-request/password-reset-request.module').then( m => m.PasswordResetRequestPageModule)
  },
  {
    path: 'password-reset-waiting',
    loadChildren: () => import('./password-reset-waiting/password-reset-waiting.module').then( m => m.PasswordResetWaitingPageModule)
  },
  {
    path: 'registration-success',
    loadChildren: () => import('./registration-success/registration-success.module').then( m => m.RegistrationSuccessPageModule)
  },
  {
    path: 'password-reset',
    loadChildren: () => import('./password-reset/password-reset.module').then(m => m.PasswordResetPageModule)
  },  {
    path: 'register-waiting',
    loadChildren: () => import('./register-waiting/register-waiting.module').then( m => m.RegisterWaitingPageModule)
  },




];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }