import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';
import { v4 as uuidv4 } from 'uuid';  // Importer la fonction v4 de uuid

@Injectable({
  providedIn: 'root'
})
export class SessionService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  createSession(userId: string, data: any): Observable<any> {
    const sessionId = uuidv4();  // Génère un nouvel UUID pour la session
    console.log('Creating session with ID:', sessionId);
    return this.http.post(`${this.apiUrl}/session/create_session`, { user_id: userId, data, session_id: sessionId });
  }

  getSession(sessionId: string): Observable<any> {
    console.log('Getting session with ID:', sessionId);
    return this.http.get(`${this.apiUrl}/session/get_session/${sessionId}`);
  }

  deleteSession(sessionId: string): Observable<any> {
    console.log('Deleting session with ID:', sessionId);
    return this.http.delete(`${this.apiUrl}/session/delete_session/${sessionId}`);
  }

  resetPasswordRequest(mail: string): Observable<any> {
    console.log('Reset password request for email:', mail);
    return this.http.post(`${this.apiUrl}/auth/reset_password_request`, { mail });
  }

  resendReset(sessionId: string): Observable<any> {
    console.log('Resending reset with session ID:', sessionId);
    return this.http.post(`${this.apiUrl}/auth/resend_reset`, { session_id: sessionId });
  }


  resetPassword(token: string, newPassword: string): Observable<any> {
    console.log('Resetting password with token:', token);
    return this.http.post(`${this.apiUrl}/auth/reset_password`, { token, new_password: newPassword });
  }
}
