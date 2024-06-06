import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth-service.service';
import { Router } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-user-popover',
  templateUrl: './user-popover.component.html',
  styleUrls: ['./user-popover.component.scss'],
})

export class UserPopoverComponent implements OnInit {
  isLoggedIn = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef // Inject ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe((loggedIn) => {
      this.isLoggedIn = loggedIn;
      this.cdr.detectChanges(); // Force change detection
    });
  }

  loginDialog() {
    this.router.navigateByUrl('/login');
  }

  login(username: string, password: string) {
    this.authService.login(username, password).subscribe({
      next: (success) => {
        this.router.navigateByUrl('/home');
      },
      error: (error) => {
        console.error('Login failed', error);
      },
    });
  }

  profile() {
    console.log('Profile clicked');
  }

  preferences() {
    console.log('Preferences clicked');
  }

  logout() {
    this.authService.logout();
    this.isLoggedIn = false;
    this.router.navigateByUrl('/home');
  }
}
