import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth-service.service';
import { SessionService } from '../services/session.service';
import { environment } from '../../environments/environment'; // Importer l'environnement

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
})
export class HomePage implements OnInit {
  sessionData: any;

  constructor(
    private sessionService: SessionService,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit() {
    const sessionId = localStorage.getItem('session_id');
    if (sessionId) {
      this.sessionService.getSession(sessionId).subscribe({
        next: (response) => {
          this.sessionData = response.session_data;
          console.log('Session data:', this.sessionData);
        },
        error: (error) => {
          console.error('Session retrieval error', error);
          this.router.navigate(['/login']);
        }
      });
    } else {
      this.router.navigate(['/login']);
    }
  }

  logout() {
    const sessionId = localStorage.getItem('session_id');
    if (sessionId) {
      this.sessionService.deleteSession(sessionId).subscribe({
        next: () => {
          localStorage.removeItem('session_id');
          this.router.navigate(['/login']);
        },
        error: (error) => {
          console.error('Logout error', error);
          this.router.navigate(['/login']);
        }
      });
    } else {
      this.router.navigate(['/login']);
    }
  }
}
