import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private isLoggedInSubject: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this.isLoggedInSubject.asObservable(); // Ajoutez un observable public

  constructor(private http: HttpClient) { }

  isLoggedIn(): boolean {
    return this.isLoggedInSubject.value;
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post('http://localhost:5000/login', { username, password }).pipe(
      tap((response) => {
        this.isLoggedInSubject.next(true);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('accessToken');
    this.isLoggedInSubject.next(false);
  }
}
