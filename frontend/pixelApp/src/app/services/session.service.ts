import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SessionService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  createSession(userId: string, data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/session/create_session`, { user_id: userId, data });
  }

  getSession(sessionId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/session/get_session/${sessionId}`);
  }

  deleteSession(sessionId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/session/delete_session/${sessionId}`);
  }

  resetPasswordRequest(mail: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/reset_password_request`, { mail });
  }

  resendReset(sessionId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/resend_reset`, { session_id: sessionId });
  }
}
