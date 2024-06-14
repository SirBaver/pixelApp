import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap, switchMap, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isLoggedInSubject: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this.isLoggedInSubject.asObservable(); // Ajoutez un observable public
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  isLoggedIn(): boolean {
    return this.isLoggedInSubject.value;
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, { username, password }).pipe(
      switchMap((response: any) => {
        // Après une connexion réussie, créez une session
        return this.createSession(response.user_id).pipe(
          tap((sessionResponse: any) => {
            // Stocker l'ID de session dans le stockage local
            localStorage.setItem('session_id', sessionResponse.session_id);
            this.isLoggedInSubject.next(true);
          })
        );
      })
    );
  }

  private createSession(userId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/session/create_session`, { user_id: userId, data: {} });
  }

  logout(): Observable<any> {
    const sessionId = localStorage.getItem('session_id');
    if (sessionId) {
      return this.http.delete(`${this.apiUrl}/session/delete_session/${sessionId}`).pipe(
        tap(() => {
          localStorage.removeItem('session_id');
          this.isLoggedInSubject.next(false);
        })
      );
    } else {
      this.isLoggedInSubject.next(false);
      return new Observable(observer => {
        observer.next();
        observer.complete();
      });
    }
  }
}
