import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-language-popover',
  templateUrl: './language-popover.component.html',
  styleUrls: ['./language-popover.component.scss'],
})
export class LanguagePopoverComponent {

  constructor(private translateService: TranslateService) { }

  changeLanguage(lang: string) {
    this.translateService.use(lang);
    // Fermez le popover ici si nécessaire
  }
}