import { Component, Inject, Renderer2 } from '@angular/core';
import { DarkModeService } from './services/dark-mode.service';
import { TranslateService } from '@ngx-translate/core';
import { DOCUMENT } from '@angular/common';
// Importez PopoverController et UserPopoverComponent
import { PopoverController } from '@ionic/angular';
import { UserPopoverComponent } from './user-popover/user-popover.component';
import { LanguagePopoverComponent } from './language-popover/language-popover.component';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent {
  darkMode = false;

  constructor(
    private darkModeService: DarkModeService, 
    private translate: TranslateService,
    private renderer: Renderer2,
    @Inject(DOCUMENT) private document: Document,
    // Ajoutez PopoverController au constructeur
    private popoverController: PopoverController
  ) {
    this.darkMode = this.darkModeService.isDarkMode();
    this.darkModeService.setDarkMode(this.darkMode); // Appliquer le mode au démarrage

    // Configuration du service de traduction
    this.translate.setDefaultLang('en');
    this.translate.use('fr');

    // Appliquer le mode sombre au démarrage si nécessaire
    if (this.darkMode) {
      this.renderer.addClass(this.document.body, 'dark');
    }
  }

  toggleDarkMode() {
    this.darkMode = !this.darkMode;
    if (this.darkMode) {
      this.renderer.addClass(this.document.body, 'dark');
      this.renderer.removeClass(this.document.body, 'light'); // Seulement si vous utilisez une classe 'light' dans votre CSS
    } else {
      this.renderer.removeClass(this.document.body, 'dark');
      this.renderer.addClass(this.document.body, 'light'); // Seulement si vous utilisez une classe 'light' dans votre CSS
    }
  }

  // Ajoutez la méthode openUserPopover ici
  async openUserPopover(event: any) {
    const popover = await this.popoverController.create({
      component: UserPopoverComponent,
      event: event,
      translucent: true
    });
    return await popover.present();
  }

  // Ajoutez la méthode openLanguagePopover ici
  async openLanguagePopover(ev: any) {
    const popover = await this.popoverController.create({
      component: LanguagePopoverComponent,
      event: ev,
      translucent: true
    });
    return await popover.present();
  }
}