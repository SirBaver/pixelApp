import { Injectable } from '@angular/core';
import { Platform } from '@ionic/angular';

@Injectable({
  providedIn: 'root'
})
export class DarkModeService {
  constructor(private platform: Platform) { }

  isDarkMode() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    return prefersDark.matches;
  }

  setDarkMode(val: boolean) {
    if (val) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }
}
