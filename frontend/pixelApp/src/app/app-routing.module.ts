import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component'; // Importez le LoginComponent ici
import { RegisterComponent } from './register/register.component'; // Importez le RegisterComponent ici

const routes: Routes = [
  {
    path: 'home',
    loadChildren: () => import('./home/home.module').then( m => m.HomePageModule)
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  { 
    path : 'login', component: LoginComponent}, // Ajoutez une route pour le LoginComponent
  { 
    path: 'register', component: RegisterComponent },   {
    path: 'preference',
    loadChildren: () => import('./preference/preference.module').then( m => m.PreferencePageModule)
  },  {
    path: 'main',
    loadChildren: () => import('./main/main.module').then( m => m.MainPageModule)
  },
  {
    path: 'profile',
    loadChildren: () => import('./profile/profile.module').then( m => m.ProfilePageModule)
  },

// Ajoutez une route pour le RegisterComponent
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }